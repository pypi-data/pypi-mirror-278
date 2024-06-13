import hashlib
import math
import shutil
import ssl
import os
import openai
import tinytag
from pydub import AudioSegment
from pytube import YouTube, Playlist
from ebooklib import epub
from typing import List
import tiktoken


ssl._create_default_https_context = ssl._create_unverified_context

MAX_SIZE = 25  # max transcription size openai


class YouTubeToKindle:
    def __init__(self, download_files: List[str] = None,
                 download_dir: str = "", openai_key: str = "",
                 model: str = 'gpt-4o', max_size: int = MAX_SIZE,
                 chunk_size: int = 512):
        """
        Initialize the Transcribe class.

        :param download_files: List of audio file paths or URLs.
        :param download_dir: Directory to download and store audio files.
        :param openai_key: API key for OpenAI.
        :param model: Model name for OpenAI.
        :param max_size: Maximum size for transcription files in MB.
        """
        self.total_cost = 0
        self.split_files = []
        self.download_files = download_files if download_files else []
        self.download_dir = download_dir
        self.client = openai.Client(api_key=openai_key)
        self.model = model
        self.max_size = max_size
        self.files_to_convert = []
        self.files_root = ""
        self.playlist = ""
        self.chunk_size = chunk_size    # size of chunks used for redrafting
        self.cost_per_second = 0.0001  # USD cost of transcription for openai
        self.rewritten_files_list = [] # list of filenames of redrafted transcriptions
        self.titles = []                # list of titles and proxy titles of videos
        self.authors = []
        self.playlist_title = ""
        self.params = {'title': 'YTK Book',
                        'author': 'youtube-to-kindle',
                        'redraft': True,
                        'turn_video_title_to_chapter_name': False,
                        'turn_first_video_title_to_book_name': False,
                        'turn_filename_root_to_chapter_name': False,
                       'turn_playlist_title_to_book_title': False,
                       'make_first_video_creator_author': False,
                       'language': 'en',
                       'encoding': 'utf-8',
                        }
        # set id as hash of book title
        self.params['identifier'] = hashlib.md5(self.params['title'].encode()).hexdigest()
        self.cost_per_token = {'gpt-4o': {'input': 0.0000005, 'output': 0.0000005}}
        self.cost_so_far = 0
        if self.model == "gpt-4o":
            self.encoding = tiktoken.encoding_for_model("gpt-4-turbo")
        elif self.model == "gpt-3.5-turbo":
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def num_tokens(self, text):
        return len(self.encoding.encode(text))

    # update total cost so far based on tokens for input or output
    def estimate_rewrite_cost(self, text: str, input: bool = True) -> None:
        direction = "input" if input else "output"
        tokens = self.num_tokens(text)
        self.total_cost += tokens * self.cost_per_token[self.model][direction]


    def set_download_dir(self, download_dir: str) -> None:
        """
        Set the download directory for audio files.

        :param download_dir: The directory to download and store audio files.
        """
        self.download_dir = download_dir

    def add_to_files(self, file: str) -> None:
        """
        Add a file to the list of files to convert (could be audio, text or youtube link).

        :param file: The file to add (could be audio or text filename, or youtube link).
        """
        # if a playlist then adds all videos in list
        if file.startswith("http") and "/playlist?" in file:
            self.download_files += [v.watch_url
                                    for v in Playlist(file).videos]
            self.playlist_title = Playlist(file).title
        else:
            self.download_files.append(file)

    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to the OpenAI model and return the response.

        :param prompt: The prompt to send.
        :return: The response from the model.
        """
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        completions = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        return completions.choices[0].message.content

    def download(self) -> None:
        """
        Download Youtube audio or copy audio to the specified directory.
        """
        print("Downloading and/or collecting audio or text...")
        for audio in self.download_files:
            print(audio)
            # must be a youtube link
            if audio.startswith("http"):
                yt = YouTube(audio)
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=self.download_dir)
                video_title = yt.title
                # remove any non alphanumeric characters
                video_title = ''.join(e for e in video_title if e.isalnum() or e.isspace())
                self.titles.append(video_title)
                base, ext = os.path.splitext(out_file)
                #if self.params['turn_video_title_to_filename_root']:
                #    # replace any forward or backward slashes with spaces
                #    video_title = video_title.replace("/", " ").replace("\\", " ")
                #    new_file = os.path.join(self.download_dir, video_title + ".mp3")
                #else:
                new_file = base + ".mp3"
                os.rename(out_file, new_file)
                self.authors.append(yt.author)
            else: # audio or text
                new_file = os.path.basename(audio)
                # make title the filename root without extension
                title = os.path.splitext(os.path.basename(audio))[0]
                self.titles.append(title)
                shutil.copy(audio, os.path.join(self.download_dir, new_file))
            self.files_to_convert.append(new_file)

    def split_mp3(self, file_path: str, chunk_size_mb: int = 0) -> None:
        """
        Split an MP3 file into chunks of approximately the specified size.

        :param file_path: Path to the MP3 file.
        :param chunk_size_mb: Size of each chunk in MB. Defaults to a fraction of max_size.
        """
        if not chunk_size_mb:
            chunk_size_mb = int(0.99 * self.max_size)
        chunk_size_bytes = chunk_size_mb * 1024 * 1024

        audio = AudioSegment.from_mp3(file_path)
        total_size_bytes = len(audio.raw_data)
        num_chunks = math.ceil(total_size_bytes / chunk_size_bytes)
        chunk_duration_ms = len(audio) / num_chunks

        split_files = []
        for i in range(num_chunks):
            start_time = i * chunk_duration_ms
            end_time = (i + 1) * chunk_duration_ms if (i + 1) * chunk_duration_ms <= len(audio) else len(audio)
            chunk = audio[start_time:end_time]
            filename = ''.join(os.path.basename(file_path).split(".")[:-1]) + f"_chunk_{i + 1}.mp3"
            filename = os.path.join('audio/split_files', filename)
            chunk.export(filename, format="mp3")
            split_files.append(filename)
            print(f"Chunk {i + 1} saved: {filename}")
        if end_time < len(audio):
            chunk = audio[end_time:]
            filename = ''.join(os.path.basename(file_path).split(".")[:-1]) + f"_chunk_{num_chunks + 1}.mp3"
            filename = os.path.join('audio/split_files', filename)
            chunk.export(filename, format="mp3")
            split_files.append(filename)
            print(f"Chunk {num_chunks + 1} saved: {filename}")
        self.split_files = split_files

    def chunk_text(self, text: str) -> List[str]:
        """
        Break down text into chunks of at least N words, ending in a full stop.

        :param text: The text to chunk.
        :param N: Minimum number of words per chunk.
        :return: List of text chunks.
        """
        sentences = text.split(".")
        chunks = []
        chunk = ""
        for sentence in sentences:
            if len(chunk.split()) < self.chunk_size:
                chunk += sentence + "."
            else:
                chunks.append(chunk)
                chunk = ""
        # if whole thing less than N words
        if not chunks:
            chunks.append(chunk)
        return chunks

    def save_chunks(self, full_transcription: str, file_path: str) -> (str, List[str]):
        """
        Save full transcription to a file as newline seperated chunks.

        :param full_transcription: Full transcription text.
        :param file_path: Path to save the chunked text file.
        :return: Path to the saved chunked text file.
        """
        chunks = self.chunk_text(full_transcription)
        chunk_file = os.path.splitext(file_path)[0] + "_chunked.txt"
        with open(chunk_file, "w") as f:
            for c in chunks:
                f.write(c + "\n")
        return chunk_file, chunks

    def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe an audio file or re-write txt.

        :param file_path: Path to the audio file.
        """
        filename = ''.join(os.path.splitext(file_path)[:-1]) + ".txt" # filename for unredrafted txt
        if file_path.endswith(".txt"):  # if a text file, don't transcribe or split
            with open(file_path,'r', encoding=self.params['encoding']) as f:
                full_transcription = f.read()
            # full_transcription now contains all text
        else: # audio file - check if needs to be split and then transcribe
            file_size = os.path.getsize(file_path)
            if file_size > self.max_size * 1024 * 1024:
                self.split_mp3(file_path)
                files = self.split_files
            else:
                files = [file_path]
            full_transcription = ""
            for file in files:
                print("Transcribing", file)
                with open(file, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en",
                    )
                print(transcription.text)
                full_transcription += transcription.text + " "
                with open(filename, "w") as f:
                    f.write(full_transcription)
        if self.params['redraft']:
            chunk_file, rewritten_chunks_list = self.save_chunks(full_transcription,
                                                                 file_path)
            rewritten_chunks_filename = self.rewrite_chunks(rewritten_chunks_list,
                                                            filename)
        else:
            rewritten_chunks_filename = filename # just point it to original text if not redrafting
        return rewritten_chunks_filename

    def get_audio_duration(self, file_path: str) -> float:
        """
        Get the duration of an audio file.

        :param file_path: Path to the audio file.
        :return: Duration of the audio file in seconds.
        """
        audio = tinytag.TinyTag.get(file_path)
        return audio.duration

    def estimate_transcription_cost(self, duration_seconds: float) -> None:
        """
        Estimate the cost of using the API.

        :param duration_seconds: Duration of the audio file in seconds.

        """

        self.total_cost += duration_seconds * self.cost_per_second


    def rewrite_chunks(self, chunks: List[str], file_path: str) -> str:
        """
        Rewrite chunks of text using the OpenAI model.

        :param chunks: List of text chunks.
        :param file_path: Path to save the rewritten text.
        """
        prompt = """
        You are a professional writer and editor who is an expert in non-fiction writing.
        Below is some text which was transcribed directly from audio.
        Please re-write so it does not read like a transcription but like a non-fiction book.
        Also add paragraphing as appropriate.
        Note: some of the text may be direct dialogue quotes from movies. You can leave these as they are.
        IMPORTANT: This is not the complete transcription, so do not re-write in a
        standalone manner. Also do not leave out ANY information.
        ONLY return the re-written text, with no preamble from yourself.
        Here is the text:
        {{"""
        output_file = os.path.splitext(file_path)[0] + "_redrafted.txt"
        rewritten_text = ""
        print("Rewriting chunks")
        for c in chunks:
            full_prompt = prompt + c + "}}"
            self.estimate_rewrite_cost(full_prompt)
            rewrite = self.send_prompt(full_prompt)
            self.estimate_rewrite_cost(rewrite, input=False)
            print(rewrite + "\n" + '-' * 50)
            rewritten_text += rewrite + "\n"
            with open(output_file, "w") as f:
                f.write(rewritten_text + "\n")
        return output_file

    def transcribe(self) -> None:
        """
        Transcribe all audio files in the download directory.
        """
        print("Transcribing audio files")
        cost = 0
        #file_range = os.listdir(self.download_dir) if self.download_dir else self.files_to_convert
        file_range = self.files_to_convert
        for file in file_range:
            if file.endswith(".mp3"):
                file = os.path.join(self.download_dir, file) if self.download_dir else file
                print(file)
                rewritten_chunks_filename = self.transcribe_audio(file)
                duration = self.get_audio_duration(file)
                self.estimate_transcription_cost(duration)
                self.rewritten_files_list.append(rewritten_chunks_filename)
            else: # text file .txt
                file = os.path.join(self.download_dir, file) if self.download_dir else file
                print(file)
                rewritten_chunks_filename = self.transcribe_audio(file)
                if file.endswith(".mp3"):
                    self.estimate_transcription_cost(duration)
                self.rewritten_files_list.append(rewritten_chunks_filename)
        #print(f"Total transcription and redraft cost: ${self.total_cost:.6f}")

    def text_to_epub(self, text_files: List[str], output_file: str) -> str:
        """
        Convert multiple text files to an EPUB format book with multiple chapters.

        :param text_files: List of paths to the text files.
        :param output_file: Path to save the EPUB file.
        :return: Path to the generated EPUB file.
        """
        book = epub.EpubBook()
        book.set_identifier(self.params['identifier']) # unique book identifier
        if self.params['turn_first_video_title_to_book_name']:
            book.set_title(self.titles[0])
        elif self.params['turn_playlist_title_to_book_title']:
            book.set_title(self.playlist_title)
        else:
            book.set_title(self.params['title'])
        book.set_language(self.params['language'])
        if self.params['make_first_video_creator_author']:
            book.add_author(self.authors[0])
        else:
            book.add_author(self.params['author'])

        spine = ['nav']
        toc = []

        for c, text_file in enumerate(text_files):
            with open(text_file, 'r', encoding='utf-8') as f:
                text_content = f.read()

            paragraphs = text_content.split('\n')
            html_content = ''.join(f'<p>{paragraph}</p>' for paragraph in paragraphs if paragraph.strip())
            if self.params['turn_video_title_to_chapter_name']:
                chapter = epub.EpubHtml(title=f'{self.titles[c]}', file_name=f'chap_{c + 1}.xhtml', lang='en')
                chapter.content = f'<h1>Chapter {c + 1} - {self.titles[c]}</h1>{html_content}'
            elif self.params['turn_filename_root_to_chapter_name']:
                base = os.path.basename(text_file)
                if base.endswith('_redrafted.txt'):
                    # remove _redrafted from the end but leave the extension
                    base = base[:-len('_redrafted.txt')] + '.txt'
                # remove the extension
                base = os.path.splitext(base)[0]
                chapter = epub.EpubHtml(title=f'Chapter {c + 1} - {base}',
                                        file_name=f'chap_{c + 1}.xhtml', lang='en')
                chapter.content = f'<h1>Chapter {c + 1} - {base}</h1>{html_content}'
            else:
                chapter = epub.EpubHtml(title=f'Chapter {c + 1}', file_name=f'chap_{c + 1}.xhtml', lang='en')
                chapter.content = f'<h1>Chapter {c + 1}</h1>{html_content}'
            book.add_item(chapter)
            spine.append(chapter)
            toc.append(chapter)
        book.spine = spine
        book.toc = toc
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(output_file, book)
        return output_file

    def load_conversion_list(self, filename: str):
        """
        Load a list of files to convert.

        :param filename: Path to the file containing the list of files.
        :return: List of file paths.
        """
        with open(filename, "r") as f:
            files = f.read().splitlines()
        self.files_root = files[0]
        self.files_to_convert = [os.path.join(self.files_root, f) for f in files[1:]]

    def make_ebook(self) -> str:
        """
        Convert all files or youtube videos in the download_files to a single EPUB format book.
        """
        print("Converting files to EPUB")
        if not self.download_dir:
            print("No download directory specified. Use set_download_dir() method.")
            return ""
        else:
            # if the download directory does not exist, create it
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
        if self.download_files:
            self.download()
        else:
            print("Add files to process using the 'add_to_files()' method.")
            return ""
        # goes through every file in the download directory and transcribes it
        # and re-drafts it
        self.transcribe()
        # writes the results to the download directory
        output_filename = os.path.join(self.download_dir,
                                       f"{self.params['title']}.epub")
        self.text_to_epub(self.rewritten_files_list,
                          output_filename)
        return output_filename

