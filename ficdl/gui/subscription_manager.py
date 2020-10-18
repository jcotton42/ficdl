import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class SubscriptionManager(tk.Frame):
    def __init__(self, master, window):
        super().__init__(master)
        self.window = window
        self.create_widgets()

    def create_widgets(self):
        row = 0
        ttk.Label(self, text='Subscribed stories').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='NOT SUPPORTED YET').grid(row=row, column=0, sticky=tk.W)
