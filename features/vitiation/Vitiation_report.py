import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db_manager
from utils import helpers as utils_helpers
from datetime import datetime
from features.vitiation.vitiation_data_exporter import export_vitiation_data_to_excel

class VitiationReportDialog(tk.Toplevel):
    def __init__(self, parent, work_id):
        super().__init__(parent)
        self.parent = parent
        self.work_id = work_id
        self.work_details = db_manager.get_work_by_id(work_id)
        self.work_name = self.work_details['work_name'] if self.work_details else "N/A"
        self.title(f"Generate Vitiation Report for: {self.work_name}")
        self.geometry("500x400") # Increased size for better visibility
        self.minsize(450, 350)
        self.transient(parent)
        self.grab_set()
        self.selected_firms = []
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text=f"Work: {self.work_name}", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Variation Selection
        variation_frame = ttk.LabelFrame(main_frame, text="Select Variation Column", padding=10)
        variation_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 10))
        self.variation_names = db_manager.get_variation_names_for_work(self.work_id)
        self.selected_variation_var = tk.StringVar()
        if self.variation_names:
            self.selected_variation_var.set(self.variation_names[0])
        self.variation_combobox = ttk.Combobox(variation_frame, textvariable=self.selected_variation_var, values=self.variation_names, state="readonly")
        self.variation_combobox.pack(fill=tk.X, padx=5, pady=5)
        if not self.variation_names:
            self.variation_combobox.set("No variations found")
            self.variation_combobox.config(state="disabled")

        firm_selection_frame = ttk.LabelFrame(main_frame, text="Select Firms for Report", padding=10)
        firm_selection_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(5, 10))
        self.firm_listbox = tk.Listbox(firm_selection_frame, selectmode=tk.MULTIPLE, exportselection=False, height=5)
        self.firm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        firm_scrollbar = ttk.Scrollbar(firm_selection_frame, orient=tk.VERTICAL, command=self.firm_listbox.yview)
        self.firm_listbox.config(yscrollcommand=firm_scrollbar.set)
        firm_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure firm_selection_frame to expand
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame, padding=5)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(button_frame, text="Generate Report", command=self._generate_report, style='Primary.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy, style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)

    def _load_data(self):
        self._load_firms()

    def _load_firms(self):
        # Load only firms that have quoted in the current work
        firms_for_work = db_manager.get_unique_firm_names_by_work_id(self.work_id)
        self.firm_listbox.delete(0, tk.END)
        for firm in firms_for_work:
            self.firm_listbox.insert(tk.END, firm)

    def _generate_report(self):
        selected_variation_name = self.selected_variation_var.get()
        if not selected_variation_name or selected_variation_name == "No variations found":
            utils_helpers.show_toast(self, "Please select a variation column.", "warning")
            return

        self.selected_firms = [self.firm_listbox.get(idx) for idx in self.firm_listbox.curselection()]
        if not self.selected_firms:
            utils_helpers.show_toast(self, "Please select at least one firm.", "warning")
            return
        
        # Load schedule items directly here, as the treeview is removed
        all_items_from_db = db_manager.get_schedule_items(self.work_id)
        processed_schedule_items = []
        item_map = {item['item_id']: dict(item) for item in all_items_from_db}
        for item_id, item_data in item_map.items():
            item_data['children'] = []
            item_data['firm_rates'] = db_manager.get_firm_rates(item_id)
            item_data['variations'] = db_manager.get_schedule_item_variations(item_id) # Load variations
            item_data['level'] = 0
        for item_id, item_data in item_map.items():
            parent_id = item_data.get('parent_item_id')
            if parent_id is not None and parent_id in item_map:
                item_map[parent_id]['children'].append(item_data)
        root_items = [item for item in item_map.values() if item.get('parent_item_id') is None]
        root_items.sort(key=lambda x: x['item_name'])

        # Recursive function to flatten the hierarchy and add sr_no
        def flatten_and_process_recursive(items_list, parent_sr_prefix=""):
            sr_counter = 1
            for item in items_list:
                current_sr_no = f"{parent_sr_prefix}.{sr_counter}" if parent_sr_prefix else str(sr_counter)
                sr_counter += 1
                processed_item = item.copy()
                processed_item['sr_no'] = current_sr_no
                processed_schedule_items.append(processed_item)
                if item['children']:
                    item['children'].sort(key=lambda x: x['item_name'])
                    flatten_and_process_recursive(item['children'], current_sr_no)
        
        flatten_and_process_recursive(root_items)

        if not processed_schedule_items:
            utils_helpers.show_toast(self, "No schedule items to report.", "warning")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{self.work_name.replace(' ', '_')}_Vitiation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self, "Report generation cancelled.", "info")
            return
        
        success, message = export_vitiation_data_to_excel(
            self.work_details,
            processed_schedule_items, # Use the locally processed items
            file_path,
            self.selected_firms,
            selected_variation_name # Pass the selected variation name
        )
        if success:
            utils_helpers.show_toast(self.parent, f"Vitiation report generated successfully: {file_path}", "success")
            self.destroy()
        else:
            utils_helpers.show_toast(self, f"Error generating report: {message}", "error")