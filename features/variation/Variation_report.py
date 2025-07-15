import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db_manager
from utils import helpers as utils_helpers
from datetime import datetime
from features.variation.variation_data_exporter import export_variation_data_to_excel 

class VariationReportDialog(tk.Toplevel):
    def __init__(self, parent, work_id):
        super().__init__(parent)
        self.parent = parent
        self.work_id = work_id
        self.work_details = db_manager.get_work_by_id(work_id)
        self.work_name = self.work_details['work_name'] if self.work_details else "N/A"
        self.title(f"Generate Variation Report for: {self.work_name}")
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
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=("sn", "description", "original_qty", "new_qty", "unit", "unit_rate", "total_cost_before", "total_cost_after"), show="headings")
        self.schedule_tree.pack(fill=tk.BOTH, expand=True)

        self.schedule_tree.heading("sn", text="SN")
        self.schedule_tree.heading("description", text="Schedule Items")
        self.schedule_tree.heading("original_qty", text="Quantity (Before Variation)")
        self.schedule_tree.heading("new_qty", text="Quantity (After Variation)")
        self.schedule_tree.heading("unit", text="Unit")
        self.schedule_tree.heading("unit_rate", text="Unit Rate")
        self.schedule_tree.heading("total_cost_before", text="Total Cost (Before Variation)")
        self.schedule_tree.heading("total_cost_after", text="Total Cost (After Variation)")

        self.schedule_tree.column("sn", width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("description", width=300, stretch=tk.YES, anchor=tk.W)
        self.schedule_tree.column("original_qty", width=120, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("new_qty", width=120, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("unit", width=80, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("unit_rate", width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("total_cost_before", width=120, stretch=tk.NO, anchor=tk.CENTER)
        self.schedule_tree.column("total_cost_after", width=120, stretch=tk.NO, anchor=tk.CENTER)
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
        self.firm_listbox.bind('<<ListboxSelect>>', self._on_firm_selection_change)

        button_frame = ttk.Frame(main_frame, padding=5)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Generate Report", command=self._generate_report, style='Primary.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy, style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)

    def _on_firm_selection_change(self, event):
        selected_indices = self.firm_listbox.curselection()
        if len(selected_indices) > 1:
            # If more than one firm is selected, deselect all but the last one
            last_selected_index = selected_indices[-1]
            self.firm_listbox.selection_clear(0, tk.END)
            self.firm_listbox.selection_set(last_selected_index)
            self.selected_firms = [self.firm_listbox.get(last_selected_index)]
        elif len(selected_indices) == 1:
            self.selected_firms = [self.firm_listbox.get(selected_indices[0])]
        else:
            self.selected_firms = []

        self._update_schedule_tree_with_firm_rates()

    def _load_data(self):
        self._load_schedule_items_with_hierarchy()
        self._load_firms()
        # Update treeview with firm rates after initial load
        self._update_schedule_tree_with_firm_rates()

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
                self.schedule_tree.insert(parent_iid, tk.END, iid=item['item_id'], values=(
                    current_sr_no,
                    display_description,
                    item['quantity'],
                    item['new_quantity'],
                    item['unit'],
                    "", # Unit Rate (will be filled dynamically)
                    "", # Total Cost Before Variation (will be filled dynamically)
                    ""  # Total Cost After Variation (will be filled dynamically)
                ))
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
        # Allow editing for 'new_qty' (#4) and 'unit_rate' (#6) columns
        if column not in ('#4', '#6'):
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
        col_index = int(column.replace('#', '')) - 1 # Convert '#N' to 0-indexed N-1

        current_values = self.schedule_tree.item(item_iid, 'values')
        current_value_str = str(current_values[col_index])

        self.edit_entry = ttk.Entry(self.schedule_tree, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, current_value_str)
        self.edit_entry.focus_set()
        self.edit_item_id = int(item_iid)
        self.edit_column_id = column # Store the column ID
        self.edit_entry.bind("<Return>", self._save_inline_edit)
        self.edit_entry.bind("<FocusOut>", self._save_inline_edit)
        self.edit_entry.bind("<Escape>", self._cancel_inline_edit)

    def _update_schedule_tree_with_firm_rates(self):
        if not self.selected_firms:
            # Clear unit rate and total cost columns if no firm is selected
            for item_id in self.schedule_tree.get_children():
                current_values = list(self.schedule_tree.item(item_id, 'values'))
                current_values[5] = "" # Unit Rate
                current_values[6] = "" # Total Cost Before
                current_values[7] = "" # Total Cost After
                self.schedule_tree.item(item_id, values=current_values)
            return

        selected_firm_name = self.selected_firms[0]

        for item in self.processed_schedule_items:
            unit_rate = 0.0
            for firm_rate in item['firm_rates']:
                if firm_rate['firm_name'] == selected_firm_name:
                    unit_rate = firm_rate['unit_rate']
                    break
            
            # Update the item's unit_rate in processed_schedule_items
            item['unit_rate'] = unit_rate

            total_cost_before = item['quantity'] * unit_rate
            total_cost_after = item['new_quantity'] * unit_rate

            # Update the Treeview
            current_values = list(self.schedule_tree.item(item['item_id'], 'values'))
            current_values[3] = item['new_quantity'] # Update New Quantity
            current_values[5] = unit_rate
            current_values[6] = total_cost_before
            current_values[7] = total_cost_after
            self.schedule_tree.item(item['item_id'], values=current_values)


    def _save_inline_edit(self, event=None):
        if not self.edit_entry:
            return

        new_value_str = self.edit_entry.get().strip()
        item_id = self.edit_item_id
        edited_column_id = self.edit_column_id
        
        # Destroy the entry widget
        self.edit_entry.destroy()
        self.edit_entry = None
        self.edit_item_id = None

        if event and hasattr(event, 'keysym') and event.keysym == 'Escape':
            utils_helpers.show_toast(self, "Inline edit cancelled.", "info")
            return

        # Determine which column was edited
        column_map = {
            '#4': {'key': 'new_quantity', 'name': "New Quantity", 'idx': 3},
            '#6': {'key': 'unit_rate', 'name': "Unit Rate", 'idx': 5}
        }
        
        edited_col_info = None
        for col_id, info in column_map.items():
            if self.schedule_tree.column(col_id, option='id') == edited_column_id:
                edited_col_info = info
                break

        if not edited_col_info:
            utils_helpers.show_toast(self, "Error: Edited column not recognized.", "error")
            return

        field_key = edited_col_info['key']
        field_name = edited_col_info['name']
        field_idx = edited_col_info['idx']

        for item in self.processed_schedule_items:
            if item['item_id'] == item_id:
                original_item_data = item # Keep a reference to the item's current state
                break
        else:
            utils_helpers.show_toast(self, "Error: Item not found in data cache.", "error")
            return

        if not new_value_str:
            utils_helpers.show_toast(self, f"{field_name} cannot be empty. Reverting to previous value.", "warning")
            # No change to item data, just refresh display
            self._update_schedule_tree_with_firm_rates()
            return

        try:
            new_value = float(new_value_str)
            if new_value < 0:
                utils_helpers.show_toast(self, f"{field_name} cannot be negative. Reverting to previous value.", "warning")
                self._update_schedule_tree_with_firm_rates() # Refresh to show original values
                return
        except ValueError:
            utils_helpers.show_toast(self, f"Invalid {field_name}. Please enter a number. Reverting to previous value.", "error")
            self._update_schedule_tree_with_firm_rates() # Refresh to show original values
            return

        for item in self.processed_schedule_items:
            if item['item_id'] == item_id:
                if field_key == 'new_quantity':
                    item['new_quantity'] = new_value
                elif field_key == 'unit_rate':
                    selected_firm_name = self.selected_firms[0] if self.selected_firms else None
                    if selected_firm_name:
                        found_firm_rate = False
                        for firm_rate_entry in item['firm_rates']:
                            if firm_rate_entry['firm_name'] == selected_firm_name:
                                firm_rate_entry['unit_rate'] = new_value
                                found_firm_rate = True
                                break
                        if not found_firm_rate:
                            item['firm_rates'].append({'firm_name': selected_firm_name, 'unit_rate': new_value})
                    else:
                        # If no firm is selected, but unit rate is edited, update the item's unit_rate directly
                        # This case should ideally not happen if firm selection is enforced
                        item['unit_rate'] = new_value
                
                # After updating the underlying data, refresh the Treeview
                self._update_schedule_tree_with_firm_rates()
                utils_helpers.show_toast(self, f"{field_name} for '{item['item_name']}' updated.", "success")
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
        if len(self.selected_firms) != 1:
            utils_helpers.show_toast(self, "Please select exactly one firm for the Variation Report.", "warning")
            return
        selected_firm_name = self.selected_firms[0]

        # Prepare data for export, including calculated total costs based on the selected firm
        export_schedule_items = []
        for item in self.processed_schedule_items:
            item_copy = item.copy()
            # Find the unit rate for the selected firm for this item
            unit_rate_for_selected_firm = 0.0
            for firm_rate in item['firm_rates']:
                if firm_rate['firm_name'] == selected_firm_name:
                    unit_rate_for_selected_firm = firm_rate['unit_rate']
                    break
            
            item_copy['unit_rate'] = unit_rate_for_selected_firm
            item_copy['total_cost_before'] = item['quantity'] * unit_rate_for_selected_firm
            item_copy['total_cost_after'] = item['new_quantity'] * unit_rate_for_selected_firm
            export_schedule_items.append(item_copy)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{self.work_name.replace(' ', '_')}_Variation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self, "Report generation cancelled.", "info")
            return
        success, message = export_variation_data_to_excel(
            self.work_details,
            export_schedule_items, # Pass the prepared items with calculated costs
            all_firm_rates_by_item, # This might not be needed in exporter if calculations are done here
            updated_quantities_dict,
            file_path,
            self.selected_firms
        )
        if success:
            utils_helpers.show_toast(self.parent, f"Variation report generated successfully: {file_path}", "success")
            self.destroy()
        else:
            utils_helpers.show_toast(self, f"Error generating report: {message}", "error")