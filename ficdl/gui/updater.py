import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

from tkinter.scrolledtext import ScrolledText

from ficdl import __version__, __version_info__

class Updater(tk.Toplevel):
    def __init__(self, master, release):
        super().__init__(master)
        self.create_widgets(release)

    def create_widgets(self, release):
        if release.version > __version_info__:
            self.title('An update is available')
            
            ttk.Label(
                self,
                text=f"You are running {__version__}.\n"
                    + f"The latest is {'.'.join(map(str, release.version))}."
            ).pack(anchor='nw')

            ttk.Label(self, text='Release notes:').pack(anchor='nw')

            release_notes = ScrolledText(self, wrap='word')
            release_notes.insert('1.0', release.release_notes)
            release_notes.pack()

            button_frame = ttk.Frame(self)
            ttk.Button(button_frame, text='Download now', command=lambda: self.open_update_page(release.download_url)).pack(side='right')
            ttk.Button(button_frame, text='Not now', command=self.destroy).pack(side='right')
            button_frame.pack()
        else:
            self.title('Up to date')

            ttk.Label(self, text="You're running the latest version.").pack(anchor='center')
            ttk.Button(self, text='OK', command=self.destroy).pack(anchor='se')

    def open_update_page(self, url):
        webbrowser.open(url)
