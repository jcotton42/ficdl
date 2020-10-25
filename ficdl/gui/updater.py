import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

from ficdl import __version__, __version_info__
from ficdl.updater import get_latest_version_and_uri

class Updater(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        latest_version, download_uri = get_latest_version_and_uri()
        if latest_version > __version_info__:
            self.title('An update is available')
            
            ttk.Label(
                self,
                text=f"You are running {__version__}.\n"
                    + f"The latest is {'.'.join(map(str, latest_version))}."
            ).pack(anchor='center')

            button_frame = ttk.Frame(self)
            ttk.Button(button_frame, text='Download now', command=lambda: self.open_update_page(download_uri)).pack(side='right')
            ttk.Button(button_frame, text='Not now', command=self.destroy).pack(side='right')
            button_frame.pack()
        else:
            self.title('Up to date')

            ttk.Label(self, text="You're running the latest version.").pack(anchor='center')
            ttk.Button(self, text='OK', command=self.destroy).pack(anchor='se')

    def open_update_page(self, url):
        webbrowser.open(url)
