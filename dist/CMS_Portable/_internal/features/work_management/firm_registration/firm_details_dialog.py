
import tkinter as tk
from tkinter import ttk, messagebox

class FirmDetailsDialog(tk.Toplevel):
    def __init__(self, parent, firm_data=None):
        super().__init__(parent)
        self.title("Firm Details")
        self.geometry("400x200")
        self.parent = parent
        self.firm_data = firm_data
        self.result = None

        self.create_widgets()
        if self.firm_data:
            self.load_firm_data()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.main_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(self.main_frame, text="Representative:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.representative_entry = ttk.Entry(self.main_frame, width=40)
        self.representative_entry.grid(row=1, column=1, sticky=tk.EW)

        ttk.Label(self.main_frame, text="Address:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(self.main_frame, width=40)
        self.address_entry.grid(row=2, column=1, sticky=tk.EW)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.on_save)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def load_firm_data(self):
        self.name_entry.insert(0, self.firm_data.get('name', ''))
        self.representative_entry.insert(0, self.firm_data.get('representative', ''))
        self.address_entry.insert(0, self.firm_data.get('address', ''))

    def on_save(self):
        name = self.name_entry.get().strip()
        representative = self.representative_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Firm name cannot be empty.")
            return

        self.result = {
            'name': name,
            'representative': representative,
            'address': address
        }
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result
