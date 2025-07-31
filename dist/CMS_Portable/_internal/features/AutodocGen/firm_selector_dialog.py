import tkinter as tk
from tkinter import ttk

class FirmSelectorDialog(tk.Toplevel):
    def __init__(self, parent, firms):
        super().__init__(parent)
        self.title("Select Firm")
        self.firms = firms
        self.selected_firm = None

        self.grab_set() # Make dialog modal
        self.transient(parent)

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Select a firm:").pack(pady=5)

        self.firm_combobox = ttk.Combobox(main_frame, values=self.firms, state="readonly")
        self.firm_combobox.pack(pady=5)
        if self.firms:
            self.firm_combobox.set(self.firms[0]) # Pre-select first firm

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Select", command=self._on_select).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _on_select(self):
        self.selected_firm = self.firm_combobox.get()
        self.destroy()

    def _on_cancel(self):
        self.selected_firm = None
        self.destroy()
