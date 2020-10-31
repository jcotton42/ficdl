import tkinter as tk
from tkinter import Label, messagebox
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

from .converter import Converter
from .downloader import Downloader
from .subscription_manager import SubscriptionManager
from .updater import Updater
from ficdl import __version__, __version_info__
from ficdl.updater import get_latest_release

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f'ficdl v{__version__}')
        self.create_menu()
        self.create_widgets()

        release = get_latest_release()
        if release.version > __version_info__:
            self.show_updater(release)

    def create_menu(self):
        menubar = tk.Menu(self, tearoff=False)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='Exit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label='Check for updates', command=lambda: self.show_updater(get_latest_release()))
        help_menu.add_command(label='About', command=self.show_about)
        menubar.add_cascade(label='Help', menu=help_menu)

        self.config(menu=menubar)

    def create_widgets(self):
        row = 0
        tk.Label(self, text="You'll need to use Ctrl+V to paste because tkinter is stupid").grid(row=row, column=0, sticky=tk.W)

        row += 1
        Downloader(self, self).grid(row=row, column=0, sticky=tk.W)

        row += 1
        Converter(self, self).grid(row=row, column=0, sticky=tk.W)

        row += 1
        SubscriptionManager(self, self).grid(row=row, column=0, sticky=tk.W)

    def show_about(self):
        messagebox.showinfo('About ficdl', f'ficdl version {__version__}\nMade by jcotton42')

    def show_updater(self, release):
        updater = Updater(self, release)
        updater.focus_set()
        self.wait_window(updater)

def gui_main():
    Gui().mainloop()
