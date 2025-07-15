import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db_manager
from utils import helpers as utils_helpers
from datetime import datetime
from features.excel_export.excel_exporter import export_vitiation_report 

class VitiationReportDialog(tk.Toplevel):
    def __init__(self, parent, work_id):
        super().__init__(parent)
        self.parent = parent
        self.work_id = work_id
        self.work_details = db_manager.get_work_by_id(work_id)
        self.work_name = self.work_details['work_name'] if self.work_details else "N/A"
        self.title(f"Generate Vitiation Report for: {self.work_name}")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.transient(parent)
        self.grab_set()
        self.processed_schedule_items = []
        self.selected_firms = []
        self.vcmd_numeric = self.register(utils_helpers.validate_numeric_input)
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text=f"Work: {self.work_name}", font=('Segoe UI', 11, 'bold')).pack(fill=tk.X, pady=(0, 10))
        schedule_frame = ttk.LabelFrame(main_frame, text="Schedule Items & New Quantities", padding=10)
        schedule_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=("description", "unit", "original_qty", "new_qty"), show="headings")
        self.schedule_tree.pack(fill=tk.BOTH, expand=True)
        self.schedule_tree.heading("description", text="Description")
        self.schedule_tree.heading("unit", text="Unit")
        self.schedule_tree.heading("original_qty", text="Original Qty")
        self.schedule_tree.heading("new_qty", text="New Qty")
        self.schedule_tree.column("description", width=350, stretch=tk.YES, anchor=tk.W)
        self.schedule_tree.column("unit", width=80, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("original_qty", width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("new_qty", width=100, stretch=tk.NO, anchor=tk.CENTER)
        vsb = ttk.Scrollbar(self.schedule_tree, orient="vertical", command=self.schedule_tree.yview)
        hsb = ttk.Scrollbar(self.schedule_tree, orient="horizontal", command=self.schedule_tree.xview)
        self.schedule_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.schedule_tree.bind("<Double-1>", self._on_tree_double_click)
        self.edit_entry = None
        self.edit_item_id = None
        firm_selection_frame = ttk.LabelFrame(main_frame, text="Select Firms for Report", padding=10)
        firm_selection_frame.pack(fill=tk.X, pady=(5, 10))
        self.firm_listbox = tk.Listbox(firm_selection_frame, selectmode=tk.MULTIPLE, exportselection=False, height=5)
        self.firm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        firm_scrollbar = ttk.Scrollbar(firm_selection_frame, orient=tk.VERTICAL, command=self.firm_listbox.yview)
        self.firm_listbox.config(yscrollcommand=firm_scrollbar.set)
        firm_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        button_frame = ttk.Frame(main_frame, padding=5)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Generate Report", command=self._generate_report, style='Primary.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy, style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)

    def _load_data(self):
        self._load_schedule_items_with_hierarchy()
        self._load_firms()

    def _load_schedule_items_with_hierarchy(self):
        for iid in self.schedule_tree.get_children():
            self.schedule_tree.delete(iid)
        self.processed_schedule_items = []
        all_items_from_db = db_manager.get_schedule_items(self.work_id)
        item_map = {item['item_id']: dict(item) for item in all_items_from_db}
        for item_id, item_data in item_map.items():
            item_data['children'] = []
            item_data['new_quantity'] = item_data['quantity']
            item_data['firm_rates'] = db_manager.get_firm_rates(item_id)
            item_data['level'] = 0
        for item_id, item_data in item_map.items():
            parent_id = item_data.get('parent_item_id')
            if parent_id is not None and parent_id in item_map:
                item_map[parent_id]['children'].append(item_data)
        root_items = [item for item in item_map.values() if item.get('parent_item_id') is None]
        root_items.sort(key=lambda x: x['item_name'])
        def insert_and_process_recursive(items_list, parent_iid="", parent_sr_prefix="", level=0):
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
                self.schedule_tree.insert(parent_iid, tk.END, iid=item['item_id'], values=(display_description, item['unit'], item['quantity'], item['new_quantity']))
                self.schedule_tree.item(item['item_id'], open=True)
                if item['children']:
                    item['children'].sort(key=lambda x: x['item_name'])
                    insert_and_process_recursive(item['children'], item['item_id'], current_sr_no, level + 1)
        insert_and_process_recursive(root_items)

    def _load_firms(self):
        all_firms = db_manager.get_all_unique_firm_names()
        self.firm_listbox.delete(0, tk.END)
        for firm in all_firms:
            self.firm_listbox.insert(tk.END, firm)

    def _on_tree_double_click(self, event):
        if self.edit_entry:
            self._save_inline_edit()
            return
        region = self.schedule_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.schedule_tree.identify_column(event.x)
        if column != '#4':  # '#4' corresponds to the 'new_qty' column
            return
        item_iid = self.schedule_tree.identify_row(event.y)
        item_data = next((item for item in self.processed_schedule_items if item['item_id'] == int(item_iid)), None)
        if item_data and item_data['quantity'] == 0:
            utils_helpers.show_toast(self, "Cannot edit quantity for category/sub-category rows.", "info")
            return
        bbox = self.schedule_tree.bbox(item_iid, column)
        if not bbox:
            return
        x, y, width, height = bbox
        current_values = self.schedule_tree.item(item_iid, 'values')
        col_index = list(self.schedule_tree["columns"]).index("new_qty")
        current_value_str = str(current_values[col_index])
        self.edit_entry = ttk.Entry(self.schedule_tree, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, current_value_str)
        self.edit_entry.focus_set()
        self.edit_item_id = int(item_iid)
        self.edit_entry.bind("<Return>", self._save_inline_edit)
        self.edit_entry.bind("<FocusOut>", self._save_inline_edit)
        self.edit_entry.bind("<Escape>", self._cancel_inline_edit)

    def _save_inline_edit(self, event=None):
        if not self.edit_entry:
            return
        new_qty_str = self.edit_entry.get().strip()
        item_id = self.edit_item_id
        self.edit_entry.destroy()
        self.edit_entry = None
        self.edit_item_id = None
        if event and hasattr(event, 'keysym') and event.keysym == 'Escape':
            utils_helpers.show_toast(self, "Inline edit cancelled.", "info")
            return
        if not new_qty_str:
            found_item = False
            for item in self.processed_schedule_items:
                if item['item_id'] == item_id:
                    item['new_quantity'] = item['quantity']
                    current_values = list(self.schedule_tree.item(item_id, 'values'))
                    current_values[3] = item['new_quantity']
                    self.schedule_tree.item(item_id, values=current_values)
                    utils_helpers.show_toast(self, f"New quantity for '{item['item_name']}' reverted to original.", "info")
                    found_item = True
                    break
            if not found_item:
                utils_helpers.show_toast(self, "Error: Item not found in data cache for empty quantity.", "error")
            return
        try:
            new_quantity = float(new_qty_str)
            if new_quantity < 0:
                utils_helpers.show_toast(self, "New Quantity cannot be negative. Reverting.", "warning")
                self._load_schedule_items_with_hierarchy()
                return
        except ValueError:
            utils_helpers.show_toast(self, "Invalid Quantity. Please enter a number. Reverting.", "error")
            self._load_schedule_items_with_hierarchy()
            return
        for item in self.processed_schedule_items:
            if item['item_id'] == item_id:
                item['new_quantity'] = new_quantity
                current_values = list(self.schedule_tree.item(item_id, 'values'))
                current_values[3] = new_quantity
                self.schedule_tree.item(item_id, values=current_values)
                utils_helpers.show_toast(self, f"New quantity for '{item['item_name']}' updated.", "success")
                break
        else:
            utils_helpers.show_toast(self, "Error: Item not found in data cache.", "error")
        self.schedule_tree.focus_set()

    def _cancel_inline_edit(self, event=None):
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None
            self.edit_item_id = None
            utils_helpers.show_toast(self, "Inline edit cancelled.", "info")
        self.schedule_tree.focus_set()

    def _generate_report(self):
        self.selected_firms = [self.firm_listbox.get(idx) for idx in self.firm_listbox.curselection()]
        if not self.selected_firms:
            utils_helpers.show_toast(self, "Please select at least one firm.", "warning")
            return
        if not self.processed_schedule_items:
            utils_helpers.show_toast(self, "No schedule items to report.", "warning")
            return
        updated_quantities_dict = {str(item['item_id']): item['new_quantity'] for item in self.processed_schedule_items}
        all_original_schedule_items = db_manager.get_schedule_items(self.work_id)
        if not all_original_schedule_items:
            utils_helpers.show_toast(self, "Failed to retrieve original schedule items from database.", "error")
            return
        all_firm_rates_by_item = {}
        for item in all_original_schedule_items:
            item_id = item['item_id']
            all_firm_rates_by_item[item_id] = db_manager.get_firm_rates(item_id)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{self.work_name.replace(' ', '_')}_Vitiation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self, "Report generation cancelled.", "info")
            return
        success, message = export_vitiation_report(
            self.work_details,
            all_original_schedule_items,
            all_firm_rates_by_item,
            updated_quantities_dict,
            file_path
        )
        if success:
            utils_helpers.show_toast(self.parent, f"Vitiation report generated successfully: {file_path}", "success")
            self.destroy()
        else:
            utils_helpers.show_toast(self, f"Error generating report: {message}", "error")