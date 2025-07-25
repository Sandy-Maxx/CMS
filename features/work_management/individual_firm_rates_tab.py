import tkinter as tk
from tkinter import ttk
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon

class IndividualFirmRatesTab(ttk.Frame):
    def __init__(self, notebook, parent_app, vcmd_numeric, load_firm_rates_callback, update_schedule_item_display_costs_callback, main_window_root, work_id_var):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.main_window_root = main_window_root
        self.vcmd_numeric = vcmd_numeric
        self.load_firm_rates_callback = load_firm_rates_callback
        self.update_schedule_item_display_costs_callback = update_schedule_item_display_costs_callback
        self.work_id_var = work_id_var # Store work_id_var
        self.current_item_id = None
        self.current_item_name = None
        self.firm_entries = []
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.item_label = ttk.Label(self, text="No item selected")
        self.item_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(self, text="Firm Rates").grid(row=1, column=0, columnspan=2, pady=(10, 5))
        self.rates_frame = ttk.Frame(self)
        self.rates_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.save_icon = load_icon("save")
        self.save_button = ttk.Button(self, image=self.save_icon, compound=tk.LEFT, command=self._save_firm_rates, style='Primary.TButton')
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.save_button_text = "Save Rates"
        self.save_button.bind("<Enter>", lambda e: self.save_button.config(text=self.save_button_text))
        self.save_button.bind("<Leave>", lambda e: self.save_button.config(text=""))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def load_firm_rates(self, item_id, item_name):
        self.current_item_id = item_id
        self.current_item_name = item_name
        self.item_label.config(text=item_name)
        for widget in self.rates_frame.winfo_children():
            widget.destroy()
        self.firm_entries = []
        firm_rates = db_manager.get_firm_rates(item_id)
        all_firms = db_manager.get_unique_firm_names_by_work_id(int(self.work_id_var.get()))
        row = 0

        # Add headers for the rate columns
        ttk.Label(self.rates_frame, text="Firm Name").grid(row=row, column=0, padx=5, pady=2, sticky="w")
        ttk.Label(self.rates_frame, text="Unit Rate").grid(row=row, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(self.rates_frame, text="Labour Rate").grid(row=row, column=2, padx=5, pady=2, sticky="w")
        row += 1

        for firm in all_firms:
            unit_rate = next((r['unit_rate'] for r in firm_rates if r['firm_name'] == firm), "")
            labour_rate = next((r['labour_rate'] for r in firm_rates if r['firm_name'] == firm), "")
            
            ttk.Label(self.rates_frame, text=firm).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            unit_entry = ttk.Entry(self.rates_frame, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
            unit_entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            unit_entry.insert(0, str(unit_rate) if unit_rate else "")

            labour_entry = ttk.Entry(self.rates_frame, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
            labour_entry.grid(row=row, column=2, padx=5, pady=2, sticky="ew")
            labour_entry.insert(0, str(labour_rate) if labour_rate else "")
            
            self.firm_entries.append((firm, unit_entry, labour_entry))
            row += 1
        self.rates_frame.grid_columnconfigure(1, weight=1)
        self.rates_frame.grid_columnconfigure(2, weight=1)

    def _save_firm_rates(self):
        if not self.current_item_id:
            utils_helpers.show_toast(self.main_window_root, "No item selected.", "warning")
            return
        success = True
        for firm, unit_entry, labour_entry in self.firm_entries:
            unit_rate_str = unit_entry.get().strip()
            labour_rate_str = labour_entry.get().strip()

            unit_rate = None
            labour_rate = None

            if unit_rate_str:
                try:
                    unit_rate = float(unit_rate_str)
                    if unit_rate < 0:
                        utils_helpers.show_toast(self.main_window_root, f"Unit Rate for {firm} cannot be negative.", "error")
                        success = False
                        continue
                except ValueError:
                    utils_helpers.show_toast(self.main_window_root, f"Invalid Unit Rate for {firm}. Please enter a number.", "error")
                    success = False
                    continue
            
            if labour_rate_str:
                try:
                    labour_rate = float(labour_rate_str)
                    if labour_rate < 0:
                        utils_helpers.show_toast(self.main_window_root, f"Labour Rate for {firm} cannot be negative.", "error")
                        success = False
                        continue
                except ValueError:
                    utils_helpers.show_toast(self.main_window_root, f"Invalid Labour Rate for {firm}. Please enter a number.", "error")
                    success = False
                    continue

            # Only upsert if at least one rate is provided
            if unit_rate is not None or labour_rate is not None:
                db_manager.upsert_firm_rate(self.current_item_id, firm, unit_rate, labour_rate)
            else:
                # If both are empty, delete the entry for this firm and item
                db_manager.delete_firm_rate_by_item_and_firm(self.current_item_id, firm)

        if success:
            utils_helpers.show_toast(self.main_window_root, f"Rates for {self.current_item_name} saved successfully.", "success")
            self.update_schedule_item_display_costs_callback()
        else:
            utils_helpers.show_toast(self.main_window_root, "Some rates could not be saved.", "error")