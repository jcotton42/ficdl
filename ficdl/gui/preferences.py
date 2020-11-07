import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

from ficdl.config import CONFIG

class Preferences(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        self.type_face = tk.StringVar(value=CONFIG.default_type_face)
        self.font_size = tk.StringVar(value=CONFIG.default_font_size)
        self.line_height = tk.StringVar(value=CONFIG.default_line_height)
        self.page_size = tk.StringVar(value=CONFIG.default_pdf_page_size)

        style_prefs = ttk.LabelFrame(self, text='Default styling options')
        style_prefs.pack()

        row = 0
        ttk.Label(style_prefs, text='Type face: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.type_face).grid(row=row, column=1)

        row += 1
        ttk.Label(style_prefs, text='Font size: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.font_size).grid(row=row, column=1)

        row += 1
        ttk.Label(style_prefs, text='Line height: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.line_height).grid(row=row, column=1)

        row += 1
        ttk.Label(style_prefs, text='Page size: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.page_size).grid(row=row, column=1)

        button_frame = ttk.Frame(self)
        button_frame.pack(side='right')
        ttk.Button(button_frame, text='Cancel', command=self.destroy).pack(side='right')
        ttk.Button(button_frame, text='Save', command=self.on_save).pack(side='right')

    def on_save(self):
        type_face = self.type_face.get().strip()
        font_size = self.font_size.get().strip()
        line_height = self.line_height.get().strip()
        page_size = self.page_size.get().strip()

        if '' in [type_face, font_size, line_height, page_size]:
            messagebox.showerror('Invalid values', 'You must provide a default for all the settings.')
            return

        CONFIG.default_type_face = type_face
        CONFIG.default_font_size = font_size
        CONFIG.default_line_height = line_height
        CONFIG.default_pdf_page_size = page_size

        CONFIG.save()
        self.destroy()
