import os
import os.path
from pathlib import Path
import queue
import tempfile
from typing import Union
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from ficdl.callbacks import ChapterDetails, InitialStoryDetails
from ficdl.downloader import DownloadOptions, download_story, OutputFormat
from ficdl.utils import make_path_safe

DOWNLOAD_STATE_CHANGED = '<<DownloadStateChanged>>'

class DownloadFinished:
    work_dir: tempfile.TemporaryDirectory
    story_path: str
    story_title: str

    def __init__(self, work_dir, story_path, story_title):
        self.work_dir = work_dir
        self.story_path = story_path
        self.story_title = story_title

class Downloader(tk.Frame):
    def __init__(self, master, window):
        super().__init__(master)
        self.window = window
        self.download_data = queue.SimpleQueue()
        self.bind(DOWNLOAD_STATE_CHANGED, self.on_download_state_changed)
        self.create_widgets()

    def create_widgets(self):
        self.url = tk.StringVar()
        self.cover_path = tk.StringVar()
        self.progress_value = tk.IntVar()

        row = 0
        ttk.Label(self, text='Download a story').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='URL: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.url).grid(row=row, column=1, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Cover to use in place of story cover:').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.cover_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_for_cover).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Progressbar(self, orient='horizontal', mode='determinate', variable=self.progress_value).grid(row=row, column=0, columnspan=2, sticky='ew')
        self.download_button = ttk.Button(self, text='Download...', command=self.on_download)
        self.download_button.grid(row=row, column=2, sticky=tk.W)

    def on_browse_for_cover(self):
        file = filedialog.askopenfilename(
            parent=self.window,
            filetypes=(
                ('All supported images', '.jpg .jpeg .png'),
                ('PNG', '.png'),
                ('JPG', '.jpg .jpeg')
            )
        )

        if file == '':
            return

        self.cover_path.set(file)

    def download_callback(self, details: Union[ChapterDetails, InitialStoryDetails]):
        # not run on the UI thread, so use events
        self.download_data.put(details)
        self.event_generate(DOWNLOAD_STATE_CHANGED)

    def ask_for_save_location(self, suggest_name):
        file = filedialog.asksaveasfilename(
            parent=self.window,
            defaultextension='.epub',
            initialfile=suggest_name,
            filetypes=(
                ('ePub (all eReaders *except* Kindle', '*.epub'),
            )
        )
        
        if file == '':
            # Cancel was clicked
            return None
        
        return file

    def on_download_state_changed(self, _event):
        while not self.download_data.empty():
            data = self.download_data.get()
            if isinstance(data, InitialStoryDetails):
                self.progress_value.set((1 / len(data.metadata.chapter_names)) * 100)
            elif isinstance(data, ChapterDetails):
                self.progress_value.set((data.chatper_number / data.chapter_count) * 100)
            elif isinstance(data, DownloadFinished):
                suggest_name = make_path_safe(data.story_title)
                save_path = self.ask_for_save_location(suggest_name)
                if save_path is not None:
                    try:
                        os.replace(data.story_path, save_path)
                    finally:
                        data.work_dir.cleanup()
                else:
                    data.work_dir.cleanup()

                self.download_button.configure(state=tk.NORMAL)
                self.progress_value.set(0)
            else:
                raise Exception("A callback case isn't being handled in the GUI: " + type(data))

    def on_download(self):
        def on_download_inner(url: str, cover: Path, work_dir: tempfile.TemporaryDirectory):
            story_path = Path(work_dir.name).joinpath('story.epub')
            story_data = download_story(DownloadOptions(
                url=url,
                format=OutputFormat.EPUB,
                output_path=story_path,
                cover_path=cover,
                dump_html_to=None,
                callback=self.download_callback,
            ))
            self.download_data.put(DownloadFinished(work_dir, story_path, story_data.title))
            self.event_generate(DOWNLOAD_STATE_CHANGED)

        url = self.url.get().strip()
        cover = self.cover_path.get().strip()

        if cover == '':
            cover = None
        else:
            cover = Path(cover)

            if not cover.exists():
                messagebox.showerror(title='Cover does not exist', message='The path you gave for the cover does not exist.')
                return

        self.download_button.configure(state=tk.DISABLED)

        work_dir = tempfile.TemporaryDirectory()

        thread = threading.Thread(target=on_download_inner, args=(url, cover, work_dir))
        thread.start()
