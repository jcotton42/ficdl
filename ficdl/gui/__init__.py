import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

from .converter import Converter
from .downloader import Downloader
from .subscription_manager import SubscriptionManager

class Gui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.window = master
        self.create_widgets()

    def create_widgets(self):
        row = 0
        Downloader(self, self.window).grid(row=row, column=0, sticky=tk.W)

        row += 1
        Converter(self, self.window).grid(row=row, column=0, sticky=tk.W)

        row += 1
        SubscriptionManager(self, self.window).grid(row=row, column=0, sticky=tk.W)

def gui_main():
    root = tk.Tk()
    root.title('ficdl')
    Gui(root).mainloop()
