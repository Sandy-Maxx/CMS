import tkinter as tk
from tkinter import ttk, filedialog
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon
from .work_editor import WorkDetailsEditor
from .work_search_bar import WorkSearchBar
from features.excel_export.excel_exporter import export_work_to_excel
from features.variation.Variation_report import VariationReportDialog
from features.vitiation.Vitiation_report import VitiationReportDialog
from datetime import datetime
from features.template_engine.template_engine_tab import TemplateEngineTab

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

        self.template_engine_tab = TemplateEngineTab(self.notebook, self)
        self.notebook.add(self.template_engine_tab, text="Template Engine")
        
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
        self.works_tree.bind("<Button-3>", self._show_work_context_menu)
        button_frame = ttk.Frame(self.works_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.add_work_icon = load_icon("add")
        self.export_work_icon = load_icon("export")

        self.add_work_button = ttk.Button(button_frame, image=self.add_work_icon, compound=tk.LEFT, command=self.add_work, style='Primary.TButton')
        self.add_work_button.pack(side=tk.LEFT, padx=5)
        self.add_work_button_text = "Add New Work"
        self.add_work_button.bind("<Enter>", lambda e: self.add_work_button.config(text=self.add_work_button_text))
        self.add_work_button.bind("<Leave>", lambda e: self.add_work_button.config(text=""))

        self.export_work_button = ttk.Button(button_frame, image=self.export_work_icon, compound=tk.LEFT, command=self.export_work, style='Info.TButton')
        self.export_work_button.pack(side=tk.LEFT, padx=5)
        self.export_work_button_text = "Export Work"
        self.export_work_button.bind("<Enter>", lambda e: self.export_work_button.config(text=self.export_work_button_text))
        self.export_work_button.bind("<Leave>", lambda e: self.export_work_button.config(text=""))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _show_work_context_menu(self, event):
        # Select item on right-click
        item_id = self.works_tree.identify_row(event.y)
        if item_id:
            self.works_tree.selection_set(item_id)
            self.works_tree.focus(item_id)
            
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Export Variation Report", command=self._export_variation_report)
            context_menu.add_command(label="Export Vitiation Report", command=self._export_vitiation_report)
            context_menu.post(event.x_root, event.y_root)

    def _export_variation_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Variation Report.", "warning")
            return
        work_id = int(selected_item[0])
        VariationReportDialog(self.root, work_id)

    def _export_vitiation_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Vitiation Report.", "warning")
            return
        work_id = int(selected_item[0])
        VitiationReportDialog(self.root, work_id)

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