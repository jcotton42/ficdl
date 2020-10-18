from pathlib import Path

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from ..downloader import download_story

class Downloader(tk.Frame):
    def __init__(self, master, window):
        super().__init__(master)
        self.window = window
        self.create_widgets()

    def create_widgets(self):
        self.url = tk.StringVar()
        self.output_path = tk.StringVar()

        row = 0
        ttk.Label(self, text='Download a story').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='URL: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.url).grid(row=row, column=1, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Download to: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.output_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Button(self, text='Download', command=self.on_download).grid(row=row, column=0, sticky=tk.W)

    def on_browse(self):
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

    def on_download(self):
        url = self.url.get().strip()
        path = self.output_path.get().strip()

        if url == '' or path == '':
            messagebox.showerror(title='Error', message='You must specify both a URL and a save path.')
            return

        path = Path(path)

        if path.suffix.casefold() != '.epub'.casefold():
            messagebox.showerror(title='Unsupported format', message='Only ePub books are supported at the moment.')
            return

        download_story(url, False, str(path))
