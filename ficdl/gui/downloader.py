import re
from typing import Union

import os.path
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from ..callbacks import ChapterDetails, InitialStoryDetails
from ..downloader import download_story

class Downloader(tk.Frame):
    def __init__(self, master, window):
        super().__init__(master)
        self.window = window
        self.create_widgets()

    def create_widgets(self):
        self.url = tk.StringVar()
        self.cover_path = tk.StringVar()
        self.output_path = tk.StringVar()
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
        ttk.Label(self, text='Download to: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.output_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_for_output).grid(row=row, column=2, sticky=tk.W)

        row += 1
        self.download_button = ttk.Button(self, text='Download', command=self.on_download)
        self.download_button.grid(row=row, column=0, sticky=tk.W)

        row += 1
        ttk.Progressbar(self, orient='horizontal', mode='determinate', variable=self.progress_value).grid(row=row, column=0, columnspan=3, sticky=tk.W)

    def on_browse_for_output(self):
        file = filedialog.asksaveasfilename(
            parent=self.window,
            defaultextension='.epub',
            filetypes=(
                ('ePub (all eReaders *except* Kindle', '*.epub'),
                ('MOBI (all Kindles)', '*.mobi'),
                ('KFX (post-2015 Kindle models)', '*.kfx'),
            )
        )
        
        if file == '':
            # Cancel was clicked
            return
        
        self.output_path.set(file)

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
        if isinstance(details, InitialStoryDetails):
            self.progress_value.set((1 / details.chapter_count) * 100)
        elif isinstance(details, ChapterDetails):
            self.progress_value.set((details.chatper_number / details.chapter_count) * 100)
        else:
            raise Exception("jcotton42 forgot to update all the callback stuff")

    def on_download(self):
        def on_download_inner(url, cover, path, download_button, callback, progress_value):
            download_story(url, cover, path, callback)
            download_button.configure(state=tk.NORMAL)
            messagebox.showinfo(title='Download finished', message='All done.')
            progress_value.set(0)

        url = self.url.get().strip()
        path = self.output_path.get().strip()
        cover = self.cover_path.get().strip()

        self.download_button.configure(state=tk.DISABLED)

        if url == '' or path == '':
            messagebox.showerror(title='Error', message='You must specify both a URL and a save path.')
            return

        if not os.path.exists(cover):
            messagebox.showerror(title='Cover does not exist', message='The path you gave for the cover does not exist.')
            return

        _, suffix = os.path.splitext(path)

        if suffix.casefold() != '.epub'.casefold():
            messagebox.showerror(title='Unsupported format', message='Only ePub books are supported at the moment.')
            return

        thread = threading.Thread(target=on_download_inner, args=(url, cover, path, self.download_button, self.download_callback, self.progress_value))
        thread.start()
