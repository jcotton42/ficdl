import tkinter as tk
import tkinter.ttk as ttk

from .converter import Converter
from .downloader import Downloader
from .subscription_manager import SubscriptionManager

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ficdl')
        self.create_widgets()

    def create_widgets(self):
        row = 0
        tk.Label(self, text="You'll need to use Ctrl+V to paste because tkinter is stupid").grid(row=row, column=0, sticky=tk.W)

        row += 1
        Downloader(self, self).grid(row=row, column=0, sticky=tk.W)

        row += 1
        Converter(self, self).grid(row=row, column=0, sticky=tk.W)

        row += 1
        SubscriptionManager(self, self).grid(row=row, column=0, sticky=tk.W)

def gui_main():
    Gui().mainloop()
