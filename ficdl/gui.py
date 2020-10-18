import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class Gui(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.window = master
        self.create_widgets()

    def create_widgets(self):
        row = 0
        self.url = tk.StringVar()
        self.download_output_path = tk.StringVar()
        self.conversion_input_path = tk.StringVar()
        self.conversion_output_path = tk.StringVar()

        ttk.Label(self, text='Download a story').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='URL: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.url).grid(row=row, column=1, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Download to path: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.download_output_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_download_path).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Button(self, text='Download', command=self.on_download).grid(row=row, column=0, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Convert an existing book').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='NOT SUPPORTED YET').grid(row=row, column=0, columnspan=3, sticky=tk.W)
        
        row += 1
        ttk.Label(self, text='Input path: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.conversion_input_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_conversion_input_path).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Output path: ').grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.conversion_output_path).grid(row=row, column=1, sticky=tk.W)
        ttk.Button(self, text='Browse...', command=self.on_browse_conversion_output_path).grid(row=row, column=2, sticky=tk.W)

        row += 1
        ttk.Button(self, text='Convert', command=self.on_convert).grid(row=row, column=0, sticky=tk.W)

        row += 1
        ttk.Label(self, text='Subscribed stories').grid(row=row, column=0, columnspan=3, sticky=tk.W)

        row += 1
        ttk.Label(self, text='NOT SUPPORTED YET').grid(row=row, column=0, sticky=tk.W)

    def on_browse_download_path(self):
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
        self.download_output_path.set(file)

    def on_download(self):
        print(self.download_output_path.get())

    def on_browse_conversion_input_path(self):
        print('Browse input')

    def on_browse_conversion_output_path(self):
        print('Browse output')

    def on_convert(self):
        print('Convert')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('ficdl')
    Gui(root).mainloop()
