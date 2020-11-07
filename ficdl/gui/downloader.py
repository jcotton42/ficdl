from dataclasses import dataclass
from ficdl.scrapers.types import StoryMetadata
from pathlib import Path
import queue
from typing import Optional, Union
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from bs4 import PageElement

from ficdl.callbacks import ChapterDetails, InitialStoryDetails
from ficdl.config import CONFIG
from ficdl.downloader import download_story, write_story
from ficdl.utils import make_path_safe
from ficdl.writers.types import OutputFormat, WriterOptions

DOWNLOAD_STATE_CHANGED = '<<DownloadStateChanged>>'

@dataclass(eq=False)
class DownloadFinished:
    text: list[list[PageElement]]
    metadata: StoryMetadata
    cover_path: Optional[Path]

@dataclass(eq=False)
class SaveFinished:
    save_path: Path

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
        self.download_progress_bar = ttk.Progressbar(self, orient='horizontal', mode='determinate', variable=self.progress_value)
        self.download_progress_bar.grid(row=row, column=0, columnspan=2, sticky='ew')
        self.download_button = ttk.Button(self, text='Download...', command=self.on_download)
        self.download_button.grid(row=row, column=2, sticky=tk.W)

    def on_browse_for_cover(self):
        file = filedialog.askopenfilename(
            parent=self.window,
            filetypes=(
                ('All supported images', '.jpg .jpeg .png'),
                ('PNG', '.png'),
                ('JPG', '.jpg .jpeg'),
            )
        )

        if file == '':
            return

        self.cover_path.set(file)

    def download_callback(self, details: Union[ChapterDetails, InitialStoryDetails]):
        # not run on the UI thread, so use events
        self.download_data.put(details)
        self.event_generate(DOWNLOAD_STATE_CHANGED)

    def ask_for_save_location(self, suggest_name: str) -> Optional[Path]:
        file = filedialog.asksaveasfilename(
            parent=self.window,
            defaultextension='.epub',
            initialfile=suggest_name,
            filetypes=(
                ('ePub (all eReaders *except* Kindle)', '.epub'),
                ('PDF', '.pdf'),
            )
        )

        if file == '':
            # Cancel was clicked
            return None

        return Path(file)

    def on_download_state_changed(self, _event):
        def save_to_disk(metadata, text, format, output_path, cover_path):
            write_story(format, WriterOptions(
                chapter_text=text,
                metadata=metadata,
                output_path=output_path,
                cover_path=cover_path,
                font_family=CONFIG.default_font_family,
                font_size=CONFIG.default_font_size,
                line_height=CONFIG.default_line_height,
                page_size=CONFIG.default_page_size,
            ))
            self.download_data.put(SaveFinished(save_path=output_path))
            self.event_generate(DOWNLOAD_STATE_CHANGED)

        while not self.download_data.empty():
            data = self.download_data.get()
            if isinstance(data, InitialStoryDetails):
                self.progress_value.set((1 / len(data.metadata.chapter_names)) * 100)
            elif isinstance(data, ChapterDetails):
                self.progress_value.set((data.chatper_number / data.chapter_count) * 100)
            elif isinstance(data, DownloadFinished):
                suggest_name = make_path_safe(data.metadata.title)
                save_path = self.ask_for_save_location(suggest_name)

                if save_path is not None:
                    self.progress_value.set(0)
                    self.download_progress_bar.configure(mode='indeterminate')
                    self.download_progress_bar.start()
                    thread = threading.Thread(target=save_to_disk, args=(
                        data.metadata,
                        data.text,
                        OutputFormat(save_path.suffix.lstrip('.').lower()),
                        save_path,
                        data.cover_path,
                    ))
                    thread.start()
                else:
                    self.progress_value.set(0)
                    self.download_button.configure(state=tk.NORMAL)
            elif isinstance(data, SaveFinished):
                self.download_button.configure(state=tk.NORMAL)
                self.download_progress_bar.stop()
                self.progress_value.set(0)
                self.download_progress_bar.configure(mode='determinate')
                messagebox.showinfo('Download finished', 'All done.')
            else:
                raise Exception("A callback case isn't being handled in the GUI: " + type(data))

    def on_download(self):
        def on_download_inner(url: str, cover: Path):
            metadata, text = download_story(url, self.download_callback)
            self.download_data.put(DownloadFinished(text=text, metadata=metadata, cover_path=cover))
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

        thread = threading.Thread(target=on_download_inner, args=(url, cover))
        thread.start()
