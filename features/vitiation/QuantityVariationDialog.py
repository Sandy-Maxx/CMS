import tkinter as tk
from tkinter import ttk
from utils.helpers import show_toast, validate_numeric_input
from database import db_manager

class QuantityVariationDialog(tk.Toplevel):
    def __init__(self, parent, work_id, item_id, parent_item_id, callback, populate_reference_firm_combobox_callback, main_app_instance, last_item_name=""):
        super().__init__(parent)
        self.work_id = work_id
        self.item_id = item_id
        self.parent_item_id = parent_item_id
        self.callback = callback
        self.populate_reference_firm_combobox_callback = populate_reference_firm_combobox_callback
        self.main_app_instance = main_app_instance
        self.existing_item_data = None
        self.existing_firm_rate = None
        self.last_item_name = last_item_name # Store the last item name
        self.work_id = work_id
        self.item_id = item_id
        self.parent_item_id = parent_item_id
        self.callback = callback
        self.populate_reference_firm_combobox_callback = populate_reference_firm_combobox_callback
        self.main_app_instance = main_app_instance
        self.existing_item_data = None
        self.existing_firm_rate = None

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

        # Firm
        ttk.Label(frame, text="Firm:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.firm_combobox = ttk.Combobox(frame, textvariable=tk.StringVar(), postcommand=self._load_firms)
        self.firm_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.firm_combobox.bind("<FocusOut>", self._on_firm_focus_out) # Allow typing custom firm

        if self.existing_item_data:
            self.item_name_entry.insert(0, self.existing_item_data['item_name'])
            self.quantity_entry.insert(0, str(self.existing_item_data['quantity']))
            self.unit_combobox.set(self.existing_item_data['unit'])
            if self.existing_firm_rate:
                self.unit_rate_entry.insert(0, str(self.existing_firm_rate['unit_rate']))
                self.firm_combobox.set(self.existing_firm_rate['firm_name'])
        elif self.last_item_name: # New: Pre-fill if adding a new item and last_item_name exists
            self.item_name_entry.insert(0, self.last_item_name)
        
        ttk.Button(frame, text="Save", command=self.save, style="Primary.TButton").grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=self.destroy, style="Secondary.TButton").grid(row=5, column=1, pady=10)
        
        frame.grid_columnconfigure(1, weight=1)

    def _load_units(self):
        units = db_manager.get_all_unique_units()
        self.unit_combobox['values'] = units

    def _on_unit_focus_out(self, event):
        # This allows the user to type a custom unit if it's not in the list
        pass

    def _load_firms(self):
        firms = db_manager.get_all_unique_firm_names()
        self.firm_combobox['values'] = firms

    def _on_firm_focus_out(self, event):
        # This allows the user to type a custom firm name if it's not in the list
        pass

    def save(self):
        item_name = self.item_name_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        unit = self.unit_combobox.get().strip()
        unit_rate_str = self.unit_rate_entry.get().strip()
        firm_name = self.firm_combobox.get().strip()

        if not item_name:
            show_toast(self, "Item Name cannot be empty!", "error")
            return
        if not quantity_str and self.parent_item_id is not None:
            show_toast(self, "Quantity cannot be empty for sub-items!", "error")
            return
        if not unit and self.parent_item_id is not None:
            show_toast(self, "Unit cannot be empty for sub-items!", "error")
            return
        if not unit_rate_str and self.parent_item_id is not None:
            show_toast(self, "Unit Rate cannot be empty for sub-items!", "error")
            return
        if not firm_name and self.parent_item_id is not None:
            show_toast(self, "Firm Name cannot be empty for sub-items!", "error")
            return

        try:
            quantity = float(quantity_str)
            if quantity < 0:
                show_toast(self, "Quantity cannot be negative!", "error")
                return
        except ValueError:
            show_toast(self, "Invalid quantity! Please enter a number.", "error")
            return

        try:
            unit_rate = float(unit_rate_str)
            if unit_rate < 0:
                show_toast(self, "Unit Rate cannot be negative!", "error")
                return
        except ValueError:
            show_toast(self, "Invalid unit rate! Please enter a number.", "error")
            return

        if self.item_id:
            # Editing existing item
            if db_manager.update_schedule_item(self.item_id, item_name, unit, quantity, self.existing_item_data['parent_item_id']):
                db_manager.upsert_firm_rate(self.item_id, firm_name, unit_rate)
                show_toast(self, "Schedule item updated successfully!", "success")
                self.main_app_instance.reference_firm_var.set(firm_name) # Set the reference firm to the one just updated
                self.callback()
                self.saved_item_name = item_name # Store the item name before destroying
                self.populate_reference_firm_combobox_callback()
                self.destroy()
            else:
                show_toast(self, "Failed to update schedule item.", "error")
        else:
            # Adding new item
            new_item_id = db_manager.add_schedule_item(self.work_id, item_name, unit, quantity, self.parent_item_id)
            if new_item_id:
                db_manager.upsert_firm_rate(new_item_id, firm_name, unit_rate)
                show_toast(self, "Schedule item added successfully!", "success")
                self.main_app_instance.reference_firm_var.set(firm_name) # Set the reference firm to the one just added
                self.callback()
                self.saved_item_name = item_name # Store the item name before destroying
                self.populate_reference_firm_combobox_callback()
                self.destroy()
            else:
                show_toast(self, "Failed to add schedule item.", "error")