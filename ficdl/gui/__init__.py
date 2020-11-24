from threading import Thread
import tkinter as tk
import tkinter.messagebox as messagebox

from ficdl import __version__, __version_info__
from ficdl.gui.converter import Converter
from ficdl.gui.downloader import Downloader
from ficdl.gui.preferences import Preferences
from ficdl.gui.subscription_manager import SubscriptionManager
from ficdl.gui.updater import Updater
from ficdl.updater import get_latest_release

UPDATE_AVAILABE = '<<UpdateAvailabe>>'

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ficdl')
        self.create_menu()
        self.create_widgets()
        self.bind(UPDATE_AVAILABE, self.show_updater)

        Thread(target=self.check_for_update).start()

    def create_menu(self):
        menubar = tk.Menu(self, tearoff=False)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='Preferences...', command=self.show_preferences)
        file_menu.add_separator()
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

    def check_for_update(self):
        release = get_latest_release()
        if release.version > __version_info__:
            self.new_release = release
            self.event_generate(UPDATE_AVAILABE)

    def show_about(self):
        messagebox.showinfo('About ficdl', f'ficdl version {__version__}\nMade by jcotton42')

    def show_preferences(self):
        Preferences(self)

    def show_updater(self, _event):
        updater = Updater(self, self.new_release)
        updater.lift()
        updater.grab_set()

def gui_main():
    Gui().mainloop()
