import tkinter as tk
from tkinter import ttk, filedialog
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon
from .work_editor import WorkDetailsEditor
from .work_search_bar import WorkSearchBar
from features.excel_export.excel_exporter import export_work_to_excel
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Construction Management System")
        self.root.geometry("800x600")
        self._create_widgets()
        self.load_works()

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.works_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.works_frame, text="Works")
        
        # Search Bar
        self.search_bar = WorkSearchBar(self.works_frame, self.load_works)
        self.search_bar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.works_frame, text="Works List", font=('Segoe UI', 11, 'bold')).pack(fill=tk.X, pady=(0, 10))
        self.works_tree = ttk.Treeview(self.works_frame, columns=("name", "description"), show="headings")
        self.works_tree.pack(fill=tk.BOTH, expand=True)
        self.works_tree.heading("name", text="Work Name")
        self.works_tree.heading("description", text="Description")
        self.works_tree.column("name", width=200, anchor=tk.W)
        self.works_tree.column("description", width=400, anchor=tk.W)
        vsb = ttk.Scrollbar(self.works_frame, orient="vertical", command=self.works_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.works_tree.configure(yscrollcommand=vsb.set)
        self.works_tree.bind("<Double-1>", self.edit_work)
        button_frame = ttk.Frame(self.works_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.add_work_icon = load_icon("add")
        self.export_work_icon = load_icon("export")
        ttk.Button(button_frame, text="Add New Work", image=self.add_work_icon, compound=tk.LEFT, command=self.add_work, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Work", image=self.export_work_icon, compound=tk.LEFT, command=self.export_work, style='Info.TButton').pack(side=tk.LEFT, padx=5)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def load_works(self, search_query=None):
        for item in self.works_tree.get_children():
            self.works_tree.delete(item)
        if search_query:
            works = db_manager.get_works_by_name(search_query)
        else:
            works = db_manager.get_works()
        for work in works:
            self.works_tree.insert("", tk.END, iid=work[0], values=(work[1], work[2]))

    def add_work(self):
        WorkDetailsEditor(self.root, None, self.load_works)

    def edit_work(self, event=None):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to edit.", "warning")
            return
        work_id = int(selected_item[0])
        WorkDetailsEditor(self.root, work_id, self.load_works)

    def export_work(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to export.", "warning")
            return
        work_id = int(selected_item[0])
        work_details = db_manager.get_work_by_id(work_id)
        if not work_details:
            utils_helpers.show_toast(self.root, "Failed to retrieve work details.", "error")
            return
        schedule_items = db_manager.get_schedule_items(work_id)
        firm_rates_by_item = {item['item_id']: db_manager.get_firm_rates(item['item_id']) for item in schedule_items}
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{work_details['work_name'].replace(' ', '_')}_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self.root, "Export cancelled.", "info")
            return
        success, message = export_work_to_excel(work_details, schedule_items, firm_rates_by_item, file_path)
        if success:
            utils_helpers.show_toast(self.root, f"Work exported successfully: {file_path}", "success")
        else:
            utils_helpers.show_toast(self.root, f"Error exporting work: {message}", "error")