import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

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
        
        print(file)
        self.output_path.set(file)

    def on_download(self):
        print(self.output_path.get())
