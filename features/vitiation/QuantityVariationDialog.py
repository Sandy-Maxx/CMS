import tkinter as tk
from tkinter import ttk
from utils.helpers import show_toast, validate_numeric_input
from database import db_manager

class QuantityVariationDialog(tk.Toplevel):
    def __init__(self, parent, work_id, item_id, parent_item_id, callback, populate_reference_firm_combobox_callback, work_details_editor_instance, last_item_name=""):
        super().__init__(parent)
        self.work_details_editor_instance = work_details_editor_instance
        self.work_id = work_id
        self.item_id = item_id
        self.parent_item_id = parent_item_id
        self.callback = callback
        self.populate_reference_firm_combobox_callback = populate_reference_firm_combobox_callback
        self.existing_item_data = None
        self.existing_firm_rate = None
        self.last_item_name = last_item_name # Store the last item name

        if self.item_id:
            self.existing_item_data = db_manager.get_schedule_item_by_id(self.item_id)
            self.title(f"Edit Schedule Item: {self.existing_item_data['item_name']}")
            # Try to get a firm rate for this item, if one exists (for pre-filling)
            firm_rates = db_manager.get_firm_rates(self.item_id)
            if firm_rates:
                self.existing_firm_rate = firm_rates[0] # Take the first one for simplicity
        else:
            self.title("Add New Schedule Item")

        self.transient(parent)
        self.grab_set()
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Item Name
        ttk.Label(frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.item_name_entry = ttk.Entry(frame)
        self.item_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Quantity
        ttk.Label(frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(frame, validate="key", validatecommand=(self.register(validate_numeric_input), '%P'))
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Unit
        ttk.Label(frame, text="Unit:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.unit_combobox = ttk.Combobox(frame, textvariable=tk.StringVar(), postcommand=self._load_units)
        self.unit_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.unit_combobox.bind("<FocusOut>", self._on_unit_focus_out) # Allow typing custom unit

        # Unit Rate
        ttk.Label(frame, text="Unit Rate:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.unit_rate_entry = ttk.Entry(frame, validate="key", validatecommand=(self.register(validate_numeric_input), '%P'))
        self.unit_rate_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Labour Rate
        ttk.Label(frame, text="Labour Rate:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.labour_rate_entry = ttk.Entry(frame, validate="key", validatecommand=(self.register(validate_numeric_input), '%P'))
        self.labour_rate_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Firm
        ttk.Label(frame, text="Firm:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.firm_combobox = ttk.Combobox(frame, textvariable=tk.StringVar(), postcommand=self._load_firms)
        self.firm_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.firm_combobox.bind("<FocusOut>", self._on_firm_focus_out) # Allow typing custom firm

        if self.existing_item_data:
            self.item_name_entry.insert(0, self.existing_item_data['item_name'])
            self.quantity_entry.insert(0, str(self.existing_item_data['quantity']))
            self.unit_combobox.set(self.existing_item_data['unit'])
            if self.existing_firm_rate:
                self.unit_rate_entry.insert(0, str(self.existing_firm_rate['unit_rate']))
                self.labour_rate_entry.insert(0, str(self.existing_firm_rate['labour_rate']))
                self.firm_combobox.set(self.existing_firm_rate['firm_name'])
        elif self.last_item_name: # New: Pre-fill if adding a new item and last_item_name exists
            self.item_name_entry.insert(0, self.last_item_name)
        
        ttk.Button(frame, text="Save", command=self.save, style="Primary.TButton").grid(row=6, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=self.destroy, style="Secondary.TButton").grid(row=6, column=1, pady=10)
        
        frame.grid_columnconfigure(1, weight=1)

    def _load_units(self):
        units = db_manager.get_all_unique_units()
        self.unit_combobox['values'] = units

    def _on_unit_focus_out(self, event):
        # This allows the user to type a custom unit if it's not in the list
        pass

    def _load_firms(self):
        # When editing an item or adding a new one, always show all registered firms
        firms = db_manager.get_all_registered_firm_names()
        self.firm_combobox['values'] = firms

    def _on_firm_focus_out(self, event):
        # This allows the user to type a custom firm name if it's not in the list
        pass

    def save(self):
        item_name = self.item_name_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        unit = self.unit_combobox.get().strip()
        unit_rate_str = self.unit_rate_entry.get().strip()
        labour_rate_str = self.labour_rate_entry.get().strip() # New line
        firm_name = self.firm_combobox.get().strip()

        if not all([item_name, quantity_str, unit, unit_rate_str, firm_name]):
            show_toast(self, "All fields are required! (Labour Rate can be blank)", "error") # Updated message
            return

        try:
            quantity = float(quantity_str)
            unit_rate = float(unit_rate_str)
            labour_rate = float(labour_rate_str) if labour_rate_str else 0.0 # New line: default to 0.0 if blank

            if quantity < 0 or unit_rate < 0 or labour_rate < 0: # Updated condition
                show_toast(self, "Quantity, Unit Rate, and Labour Rate cannot be negative!", "error") # Updated message
                return
        except ValueError:
            show_toast(self, "Invalid quantity, unit rate, or labour rate! Please enter a number.", "error") # Updated message
            return

        if self.item_id:
            success = db_manager.update_schedule_item(self.item_id, item_name, unit, quantity, self.parent_item_id)
            if success:
                db_manager.upsert_firm_rate(self.item_id, firm_name, unit_rate, labour_rate) # Updated call
                show_toast(self, "Schedule item updated successfully!", "success")
        else:
            new_item_id = db_manager.add_schedule_item(self.work_id, item_name, unit, quantity, self.parent_item_id)
            if new_item_id:
                db_manager.upsert_firm_rate(new_item_id, firm_name, unit_rate, labour_rate) # Updated call
                
                # Initialize variations for the new item
                variation_names = db_manager.get_variation_names_for_work(self.work_id)
                for v_name in variation_names:
                    db_manager.add_schedule_item_variation(new_item_id, v_name, 0.0) # Initialize with 0.0

                show_toast(self, "Schedule item added successfully!", "success")
                self.item_id = new_item_id # So that the rest of the logic works as if we were editing
            else:
                show_toast(self, "Failed to add schedule item.", "error")
                return

        self.work_details_editor_instance.reference_firm_var.set(firm_name)
        if self.callback:
            self.callback()
        if self.populate_reference_firm_combobox_callback:
            self.populate_reference_firm_combobox_callback()
        self.saved_item_name = item_name
        self.destroy()