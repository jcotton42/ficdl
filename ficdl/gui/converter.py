import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class Converter(tk.Frame):
    def __init__(self, master, window):
        super().__init__(master)
        self.window = window
        self.create_widgets()

    def create_widgets(self):
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        row = 0
        ttk.Label(self, text='Convert an existing book').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='NOT SUPPORTED YET').grid(row=row, column=0, columnspan=3, sticky=tk.W)
        
        row += 1
        ttk.Label(self, text='Input path: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.input_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_input_path).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Output path: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.output_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_output_path).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Button(self, text='Convert', command=self.on_convert).grid(row=row, column=0, sticky=tk.W)

    def on_browse_input_path(self):
        print('Browse input')

    def on_browse_output_path(self):
        print('Browse output')

    def on_convert(self):
        print('Convert')
