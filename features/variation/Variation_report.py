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
        self.selected_firms = []
        self._create_widgets()
        

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text=f"Work: {self.work_name}", font=('Segoe UI', 11, 'bold')).pack(fill=tk.X, pady=(0, 10))

        # Variation Selection
        variation_frame = ttk.LabelFrame(main_frame, text="Select Variation Column", padding=10)
        variation_frame.pack(fill=tk.X, pady=(5, 10))
        self.variation_names = db_manager.get_variation_names_for_work(self.work_id)
        self.selected_variation_var = tk.StringVar()
        if self.variation_names:
            self.selected_variation_var.set(self.variation_names[0])
        self.variation_combobox = ttk.Combobox(variation_frame, textvariable=self.selected_variation_var, values=self.variation_names, state="readonly")
        self.variation_combobox.pack(fill=tk.X, padx=5, pady=5)
        if not self.variation_names:
            self.variation_combobox.set("No variations found")
            self.variation_combobox.config(state="disabled")

        firm_selection_frame = ttk.LabelFrame(main_frame, text="Select Firm for Report", padding=10)
        firm_selection_frame.pack(fill=tk.X, pady=(5, 10))
        self.firm_listbox = tk.Listbox(firm_selection_frame, selectmode=tk.SINGLE, exportselection=False, height=5)
        self.firm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        firm_scrollbar = ttk.Scrollbar(firm_selection_frame, orient=tk.VERTICAL, command=self.firm_listbox.yview)
        self.firm_listbox.config(yscrollcommand=firm_scrollbar.set)

        # Populate firms directly in _create_widgets
        all_firms = db_manager.get_unique_firm_names_by_work_id(self.work_id)
        self.firm_listbox.delete(0, tk.END)
        for firm in all_firms:
            self.firm_listbox.insert(tk.END, firm)

        button_frame = ttk.Frame(main_frame, padding=5)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Generate Report", command=self._generate_report, style='Primary.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy, style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)

    

    def _generate_report(self):
        selected_indices = self.firm_listbox.curselection()
        if not selected_indices:
            utils_helpers.show_toast(self, "Please select a firm.", "warning")
            return
        
        selected_firm_name = self.firm_listbox.get(selected_indices[0])
        self.selected_firms = [selected_firm_name]

        
        all_items_from_db = db_manager.get_schedule_items(self.work_id)
        processed_schedule_items = []
        item_map = {item['item_id']: dict(item) for item in all_items_from_db}
        for item_id, item_data in item_map.items():
            item_data['children'] = []
            item_data['new_quantity'] = item_data['quantity']  # Initialize new_quantity with original quantity
            item_data['firm_rates'] = db_manager.get_firm_rates(item_id)
            item_data['level'] = 0
        for item_id, item_data in item_map.items():
            parent_id = item_data.get('parent_item_id')
            if parent_id is not None and parent_id in item_map:
                item_map[parent_id]['children'].append(item_data)
        root_items = [item for item in item_map.values() if item.get('parent_item_id') is None]
        root_items.sort(key=lambda x: x['item_name'])

        # Recursive function to flatten the hierarchy and add sr_no and varied quantity
        def flatten_and_process_recursive(items_list, parent_sr_prefix=""):
            sr_counter = 1
            for item in items_list:
                current_sr_no = f"{parent_sr_prefix}.{sr_counter}" if parent_sr_prefix else str(sr_counter)
                sr_counter += 1
                processed_item = item.copy()
                processed_item['sr_no'] = current_sr_no

                # Apply variation if selected
                selected_variation_name = self.selected_variation_var.get()
                if selected_variation_name and selected_variation_name != "No variations found":
                    variations = db_manager.get_schedule_item_variations(item['item_id'])
                    if selected_variation_name in variations:
                        processed_item['new_quantity'] = variations[selected_variation_name]
                
                # Calculate total costs for the selected firm
                unit_rate_for_selected_firm = 0.0
                for firm_rate in processed_item['firm_rates']:
                    if firm_rate['firm_name'] == selected_firm_name:
                        unit_rate_for_selected_firm = firm_rate['unit_rate']
                        break
                
                processed_item['unit_rate'] = unit_rate_for_selected_firm
                processed_item['total_cost_before'] = processed_item['quantity'] * unit_rate_for_selected_firm
                processed_item['total_cost_after'] = processed_item['new_quantity'] * unit_rate_for_selected_firm

                processed_schedule_items.append(processed_item)
                if item['children']:
                    item['children'].sort(key=lambda x: x['item_name'])
                    flatten_and_process_recursive(item['children'], current_sr_no)
        
        flatten_and_process_recursive(root_items)

        if not processed_schedule_items:
            utils_helpers.show_toast(self, "No schedule items to report.", "warning")
            return

        # Pass processed_schedule_items directly to the exporter
        export_schedule_items = processed_schedule_items

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
            file_path,
            self.selected_firms
        )
        if success:
            utils_helpers.show_toast(self.parent, f"Variation report generated successfully: {file_path}", "success")
            self.destroy()
        else:
            utils_helpers.show_toast(self, f"Error generating report: {message}", "error")