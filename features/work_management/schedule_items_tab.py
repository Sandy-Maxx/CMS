import tkinter as tk
from tkinter import ttk
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon
from features.vitiation.QuantityVariationDialog import QuantityVariationDialog
from features.work_management.variation_manager import VariationManager

class ScheduleItemsTab(ttk.Frame):
    def __init__(self, notebook, parent_app, work_id_var, reference_firm_var, vcmd_numeric, load_firm_rates_callback, update_schedule_item_display_costs_callback, populate_reference_firm_combobox_callback, main_window_root):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.main_window_root = main_window_root
        self.work_id_var = work_id_var
        self.reference_firm_var = reference_firm_var
        self.vcmd_numeric = vcmd_numeric
        self.load_firm_rates_callback = load_firm_rates_callback
        self.update_schedule_item_display_costs_callback = update_schedule_item_display_costs_callback
        self.populate_reference_firm_combobox_callback = populate_reference_firm_combobox_callback
        self.processed_schedule_items = []
        self.last_item_name = "" # New: To store the last entered item name
        self.variation_manager = VariationManager(self, self.work_id_var.get())
        self._create_widgets()
        self._load_schedule_items()

    def _create_widgets(self):
        ttk.Label(self, text="Reference Firm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.reference_firm_combobox = ttk.Combobox(self, textvariable=self.reference_firm_var, state="readonly")
        self.reference_firm_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.reference_firm_combobox.bind("<<ComboboxSelected>>", lambda e: self._load_schedule_items())
        ttk.Label(self, text="Schedule Items").grid(row=1, column=0, columnspan=2, pady=(10, 5))
        self.schedule_tree = ttk.Treeview(self, columns=("description", "quantity", "unit", "unit_rate", "total_cost"), show="tree headings")
        self.schedule_tree.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.schedule_tree.heading("#0", text="Sr.No")
        self.schedule_tree.heading("description", text="Description")
        self.schedule_tree.heading("quantity", text="Quantity")
        self.schedule_tree.heading("unit", text="Unit")
        self.schedule_tree.heading("unit_rate", text="Unit Rate")
        self.schedule_tree.heading("total_cost", text="Total Cost")
        self.schedule_tree.column("#0", width=80, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("description", width=250, stretch=tk.YES, anchor=tk.W)
        self.schedule_tree.column("quantity", width=80, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("unit", width=70, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("unit_rate", width=90, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("total_cost", width=100, stretch=tk.NO, anchor=tk.CENTER)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.schedule_tree.yview)
        vsb.grid(row=2, column=2, sticky="ns")
        self.schedule_tree.configure(yscrollcommand=vsb.set)
        self.schedule_tree.bind("<Double-1>", self._on_double_click)
        self.schedule_tree.bind("<Button-3>", self._show_context_menu)
        self.schedule_tree.bind("<Button-3>", self._show_header_context_menu, add='+')
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        self.add_icon = load_icon("add")
        self.edit_icon = load_icon("edit")
        self.delete_icon = load_icon("delete")
        self.variation_icon = load_icon("variation")

        self.add_item_button = ttk.Button(button_frame, image=self.add_icon, compound=tk.LEFT, command=self._add_new_item, style='Primary.TButton')
        self.add_item_button.pack(side=tk.LEFT, padx=5)
        self.add_item_button_text = "Add New Item"
        self.add_item_button.bind("<Enter>", lambda e: self.add_item_button.config(text=self.add_item_button_text))
        self.add_item_button.bind("<Leave>", lambda e: self.add_item_button.config(text=""))

        self.edit_firm_rates_button = ttk.Button(button_frame, image=self.edit_icon, compound=tk.LEFT, command=self._edit_firm_rates, style='Info.TButton')
        self.edit_firm_rates_button.pack(side=tk.LEFT, padx=5)
        self.edit_firm_rates_button_text = "Edit Firm Rates"
        self.edit_firm_rates_button.bind("<Enter>", lambda e: self.edit_firm_rates_button.config(text=self.edit_firm_rates_button_text))
        self.edit_firm_rates_button.bind("<Leave>", lambda e: self.edit_firm_rates_button.config(text=""))

        self.add_variation_button = ttk.Button(button_frame, image=self.variation_icon, compound=tk.LEFT, command=self.variation_manager.add_variation_column, style='Primary.TButton')
        self.add_variation_button.pack(side=tk.LEFT, padx=5)
        self.add_variation_button_text = "Add Variation"
        self.add_variation_button.bind("<Enter>", lambda e: self.add_variation_button.config(text=self.add_variation_button_text))
        self.add_variation_button.bind("<Leave>", lambda e: self.add_variation_button.config(text=""))
        self.add_variation_button.pack(side=tk.LEFT, padx=5)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Add Sub-Item", image=self.add_icon, compound=tk.LEFT, command=self._add_sub_item)
        self.context_menu.add_command(label="Edit Item", image=self.edit_icon, compound=tk.LEFT, command=self._edit_item)
        self.context_menu.add_command(label="Delete Item", image=self.delete_icon, compound=tk.LEFT, command=self._delete_item)
        self.context_menu.add_command(label="Edit Firm Rates", image=self.edit_icon, compound=tk.LEFT, command=self._edit_firm_rates)

        self.header_context_menu = tk.Menu(self, tearoff=0)
        self.header_context_menu.add_command(label="Delete Variation", image=self.delete_icon, compound=tk.LEFT, command=self._delete_variation)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _show_header_context_menu(self, event):
        region = self.schedule_tree.identify("region", event.x, event.y)
        if region == "heading":
            column_id = self.schedule_tree.identify_column(event.x)
            column_name = self.schedule_tree.heading(column_id)["text"]
            if column_name in self.variation_manager.get_variation_names():
                self.header_context_menu.post(event.x_root, event.y_root)
                self.header_context_menu.entryconfigure(0, command=lambda: self._delete_variation(column_name))

    def _delete_variation(self, variation_name):
        self.variation_manager.delete_variation(variation_name)

    def _show_context_menu(self, event):
        item = self.schedule_tree.identify_row(event.y)
        if item:
            self.schedule_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _on_double_click(self, event):
        self.variation_manager.on_cell_edit(event)

    def _add_new_item(self):
        dialog = QuantityVariationDialog(self, self.work_id_var.get(), None, None, self._load_schedule_items, self.populate_reference_firm_combobox_callback, self.parent_app, self.last_item_name)
        self.main_window_root.wait_window(dialog)
        if hasattr(dialog, 'saved_item_name') and dialog.saved_item_name: # Check if an item was actually added/saved
            self.last_item_name = dialog.saved_item_name

    def _add_sub_item(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.main_window_root, "Please select an item to add a sub-item.", "warning")
            return
        parent_item_id = selected_item[0]
        dialog = QuantityVariationDialog(self, self.work_id_var.get(), None, parent_item_id, self._load_schedule_items, self.populate_reference_firm_combobox_callback, self.parent_app, self.last_item_name)
        self.main_window_root.wait_window(dialog)
        if hasattr(dialog, 'saved_item_name') and dialog.saved_item_name: # Check if an item was actually added/saved
            self.last_item_name = dialog.saved_item_name

    def _edit_item(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.main_window_root, "Please select an item to edit.", "warning")
            return
        item_id = selected_item[0]
        QuantityVariationDialog(self, self.work_id_var.get(), item_id, None, self._load_schedule_items, self.populate_reference_firm_combobox_callback, self.parent_app)

    def _delete_item(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.main_window_root, "Please select an item to delete.", "warning")
            return
        item_id = selected_item[0]
        if db_manager.delete_schedule_item(item_id):
            utils_helpers.show_toast(self.main_window_root, "Item deleted successfully.", "success")
            self._load_schedule_items()
        else:
            utils_helpers.show_toast(self.main_window_root, "Failed to delete item.", "error")

    def _edit_firm_rates(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.main_window_root, "Please select an item to edit firm rates.", "warning")
            return
        item_id = selected_item[0]
        item_name = self.schedule_tree.item(item_id, "text")
        self.load_firm_rates_callback(item_id, item_name)

    def _load_schedule_items(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        self.processed_schedule_items = []
        work_id = self.work_id_var.get()
        if not work_id:
            return

        base_columns = ["description", "quantity", "unit", "unit_rate", "total_cost"]
        variation_names = db_manager.get_variation_names_for_work(work_id)
        self.schedule_tree["columns"] = base_columns + variation_names

        self.schedule_tree.heading("description", text="Description")
        self.schedule_tree.heading("quantity", text="Quantity")
        self.schedule_tree.heading("unit", text="Unit")
        self.schedule_tree.heading("unit_rate", text="Unit Rate")
        self.schedule_tree.heading("total_cost", text="Total Cost")

        for v_name in variation_names:
            self.schedule_tree.heading(v_name, text=v_name)
            self.schedule_tree.column(v_name, width=90, stretch=tk.NO, anchor=tk.CENTER)

        all_items_from_db = db_manager.get_schedule_items(work_id)
        item_map = {item['item_id']: dict(item) for item in all_items_from_db}
        for item_id, item_data in item_map.items():
            item_data['children'] = []
            item_data['level'] = 0
            item_data['firm_rates'] = db_manager.get_firm_rates(item_id)
            item_data['variations'] = db_manager.get_schedule_item_variations(item_id)
            reference_firm = self.reference_firm_var.get()
            display_cost = next((rate['unit_rate'] * item_data['quantity'] for rate in item_data['firm_rates'] if rate['firm_name'] == reference_firm), 0)
            item_data['display_cost'] = display_cost
        for item_id, item_data in item_map.items():
            parent_id = item_data.get('parent_item_id')
            if parent_id is not None and parent_id in item_map:
                item_map[parent_id]['children'].append(item_data)
        root_items = [item for item in item_map.values() if item.get('parent_item_id') is None]
        root_items.sort(key=lambda x: x['item_name'])

        def insert_item_recursive(items_list, parent_iid="", parent_sr_prefix="", level=0):
            sr_counter = 1
            for item in items_list:
                current_sr_no = f"{parent_sr_prefix}.{sr_counter}" if parent_sr_prefix else str(sr_counter)
                sr_counter += 1
                processed_item = item.copy()
                processed_item['level'] = level
                processed_item['sr_no'] = current_sr_no
                self.processed_schedule_items.append(processed_item)
                indent = "    " * level
                display_description = f"{indent}{item['item_name']}"
                
                reference_firm = self.reference_firm_var.get()
                unit_rate = next((rate['unit_rate'] for rate in item['firm_rates'] if rate['firm_name'] == reference_firm), 0)
                
                total_cost = unit_rate * item['quantity']
                
                variation_values = [item['variations'].get(v_name, 0) for v_name in variation_names]

                values = (display_description, item['quantity'], item['unit'], utils_helpers.format_currency_inr(unit_rate), utils_helpers.format_currency_inr(total_cost)) + tuple(variation_values)
                self.schedule_tree.insert(parent_iid, tk.END, iid=item['item_id'], text=current_sr_no, values=values)
                self.schedule_tree.item(item['item_id'], open=True) # Expand the item
                if item['children']:
                    item['children'].sort(key=lambda x: x['item_name'])
                    insert_item_recursive(item['children'], item['item_id'], current_sr_no, level + 1)

        insert_item_recursive(root_items)

    def get_processed_schedule_items(self):
        return self.processed_schedule_items

    def get_schedule_tree(self):
        return self.schedule_tree

    def get_reference_firm_combobox(self):
        return self.reference_firm_combobox

    def get_reference_firm_var(self):
        return self.reference_firm_var

    def get_vcmd_numeric(self):
        return self.vcmd_numeric

    def get_load_firm_rates_callback(self):
        return self.load_firm_rates_callback

    def get_update_schedule_item_display_costs_callback(self):
        return self.update_schedule_item_display_costs_callback

    def get_populate_reference_firm_combobox_callback(self):
        return self.populate_reference_firm_combobox_callback

    def get_parent_app(self):
        return self.parent_app

    def get_work_id_var(self):
        return self.work_id_var

    def get_last_item_name(self):
        return self.last_item_name

    def set_last_item_name(self, name):
        self.last_item_name = name

    def get_selected_item_id(self):
        selected_item = self.schedule_tree.selection()
        if selected_item:
            return int(selected_item[0])
        return None

    def get_selected_item_name(self):
        selected_item = self.schedule_tree.selection()
        if selected_item:
            return self.schedule_tree.item(selected_item[0], "text")
        return None
