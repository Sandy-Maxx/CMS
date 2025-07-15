import tkinter as tk
from tkinter import ttk

class WorkSearchBar(ttk.Frame):
    def __init__(self, parent, search_callback):
        super().__init__(parent)
        self.search_callback = search_callback

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)

        search_label = ttk.Label(self, text="Search Work:")
        search_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    def _on_search_change(self, *args):
        self.search_callback(self.search_var.get())