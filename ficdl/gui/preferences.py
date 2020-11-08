import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

from ficdl.config import CONFIG
from ficdl.writers.types import OutputFormat
from ficdl.utils import get_font_families

class Preferences(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.tool_paths = self.create_tool_vars()

        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        self.font_family = tk.StringVar(value=CONFIG.default_font_family)
        self.font_size = tk.StringVar(value=CONFIG.default_font_size)
        self.line_height = tk.StringVar(value=CONFIG.default_line_height)
        self.page_size = tk.StringVar(value=CONFIG.default_page_size)

        style_prefs = ttk.LabelFrame(self, text='Default styling options')
        style_prefs.pack(fill='x')

        row = 0
        ttk.Label(style_prefs, text='Font family: ').grid(row=row, column=0, sticky='w')
        ttk.Combobox(style_prefs, values=get_font_families(self), textvariable=self.font_family, state='readonly').grid(row=row, column=1, sticky='ew')

        row += 1
        ttk.Label(style_prefs, text='Font size: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.font_size).grid(row=row, column=1, sticky='ew')

        row += 1
        ttk.Label(style_prefs, text='Line height: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.line_height).grid(row=row, column=1, sticky='ew')

        row += 1
        ttk.Label(style_prefs, text='Page size: ').grid(row=row, column=0, sticky='w')
        ttk.Entry(style_prefs, textvariable=self.page_size).grid(row=row, column=1, sticky='ew')

        tool_prefs = ttk.LabelFrame(self, text='Tool paths (leave blank for auto-detect)')
        tool_prefs.pack(fill='x')

        row = 0
        for tool in sorted(self.tool_paths.keys()):
            ttk.Label(tool_prefs, text=f'{tool}: ').grid(row=row, column=0, sticky='w')
            ttk.Entry(tool_prefs, textvariable=self.tool_paths[tool]).grid(row=row, column=1, sticky='ew')
            ttk.Button(
                tool_prefs,
                text='Browse...',
                command=lambda var=self.tool_paths[tool]: self.on_browse(var)
            ).grid(row=row, column=2, sticky='w')

            row += 1

        button_frame = ttk.Frame(self)
        button_frame.pack(side='right', fill='x')
        ttk.Button(button_frame, text='Cancel', command=self.destroy).pack(side='right')
        ttk.Button(button_frame, text='Save', command=self.on_save).pack(side='right')

    def create_tool_vars(self) -> dict[str, tk.StringVar]:
        tool_vars = {}
        for tool in (format.tool for format in OutputFormat.__members__.values()):
            path = CONFIG.tool_paths.get(tool, None)
            if path is not None:
                var = tk.StringVar(value=str(path))
            else:
                var = tk.StringVar()

            tool_vars[tool] = var
        return tool_vars

    def on_browse(self, var: tk.StringVar):
        file = filedialog.askopenfilename(parent=self)

        if file != '':
            var.set(file)

    def on_save(self):
        font_family = self.font_family.get().strip()
        font_size = self.font_size.get().strip()
        line_height = self.line_height.get().strip()
        page_size = self.page_size.get().strip()

        if '' in [font_family, font_size, line_height, page_size]:
            messagebox.showerror('Invalid values', 'You must provide a default for all the formatting settings.')
            return

        for tool, path in self.tool_paths.items():
            path = path.get().strip()
            if path != '':
                CONFIG.tool_paths[tool] = path
            else:
                CONFIG.tool_paths.pop(tool, None)

        CONFIG.default_font_family = font_family
        CONFIG.default_font_size = font_size
        CONFIG.default_line_height = line_height
        CONFIG.default_page_size = page_size

        CONFIG.save()
        self.destroy()
