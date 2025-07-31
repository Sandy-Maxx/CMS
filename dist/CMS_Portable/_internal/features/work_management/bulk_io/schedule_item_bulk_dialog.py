
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .schedule_item_bulk_manager import ScheduleItemBulkManager
from database import db_manager
from utils.helpers import show_toast

class ScheduleItemBulkIODialog(tk.Toplevel):
    def __init__(self, parent, main_window_instance):
        super().__init__(parent)
        self.title("Bulk Import/Export Schedule Items")
        self.parent = parent
        self.main_window_instance = main_window_instance
        self.schedule_item_bulk_manager = ScheduleItemBulkManager()
        self.selected_work_id = None
        self._create_widgets()
        self._load_works_dropdown()

    def _create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20)

        # Work Selection
        work_selection_frame = ttk.LabelFrame(main_frame, text="Select Work")
        work_selection_frame.pack(pady=10, fill=tk.X)

        ttk.Label(work_selection_frame, text="Work:").pack(side=tk.LEFT, padx=5, pady=5)
        self.work_var = tk.StringVar()
        self.work_dropdown = ttk.Combobox(work_selection_frame, textvariable=self.work_var, state="readonly")
        self.work_dropdown.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        self.work_dropdown.bind("<<ComboboxSelected>>", self._on_work_selected)

        # Import Section
        import_frame = ttk.LabelFrame(main_frame, text="Import Schedule Items")
        import_frame.pack(pady=10, fill=tk.X)

        ttk.Label(import_frame, text="Select file to import:").pack(pady=5)
        self.import_file_path = ttk.Entry(import_frame, width=50)
        self.import_file_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(import_frame, text="Browse", command=self._browse_import_file).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(import_frame, text="Import Excel", command=self._import_excel).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(import_frame, text="Import CSV", command=self._import_csv).pack(side=tk.LEFT, padx=5, pady=5)

        # Export Section
        export_frame = ttk.LabelFrame(main_frame, text="Export Schedule Items")
        export_frame.pack(pady=10, fill=tk.X)

        ttk.Label(export_frame, text="Select export location:").pack(pady=5)
        self.export_file_path = ttk.Entry(export_frame, width=50)
        self.export_file_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(export_frame, text="Browse", command=self._browse_export_location).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(export_frame, text="Export Excel", command=self._export_excel).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(export_frame, text="Export CSV", command=self._export_csv).pack(side=tk.LEFT, padx=5, pady=5)

    def _load_works_dropdown(self):
        works = db_manager.get_works()
        self.work_map = {f"{work[1]} (ID: {work[0]})": work[0] for work in works}
        self.work_dropdown['values'] = list(self.work_map.keys())
        if works:
            self.work_var.set(list(self.work_map.keys())[0])
            self.selected_work_id = works[0][0]

    def _on_work_selected(self, event):
        selected_work_display = self.work_var.get()
        self.selected_work_id = self.work_map.get(selected_work_display)

    def _browse_import_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.import_file_path.delete(0, tk.END)
            self.import_file_path.insert(0, file_path)

    def _browse_export_location(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.export_file_path.delete(0, tk.END)
            self.export_file_path.insert(0, file_path)

    def _import_excel(self):
        if not self.selected_work_id:
            show_toast(self, "Please select a Work first.", "error")
            return

        file_path = self.import_file_path.get()
        if not file_path:
            show_toast(self, "Please select an Excel file to import.", "warning")
            return
        
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            show_toast(self, "Selected file is not an Excel file.", "error")
            return

        success, message = self.schedule_item_bulk_manager.import_schedule_items_from_excel(file_path, self.selected_work_id)
        show_toast(self, message, "success" if success else "error")
        if success and hasattr(self.main_window_instance, 'load_works'):
            self.main_window_instance.load_works() # Refresh the works list in the main window

    def _export_excel(self):
        if not self.selected_work_id:
            show_toast(self, "Please select a Work first.", "error")
            return

        file_path = self.export_file_path.get()
        if not file_path:
            show_toast(self, "Please select a location to save the Excel file.", "warning")
            return
        
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            file_path += ".xlsx" # Ensure correct extension

        success, message = self.schedule_item_bulk_manager.export_schedule_items_to_excel(file_path, self.selected_work_id)
        show_toast(self, message, "success" if success else "error")

    def _import_csv(self):
        if not self.selected_work_id:
            show_toast(self, "Please select a Work first.", "error")
            return

        file_path = self.import_file_path.get()
        if not file_path:
            show_toast(self, "Please select a CSV file to import.", "warning")
            return
        
        if not file_path.lower().endswith('.csv'):
            show_toast(self, "Selected file is not a CSV file.", "error")
            return

        success, message = self.schedule_item_bulk_manager.import_schedule_items_from_csv(file_path, self.selected_work_id)
        show_toast(self, message, "success" if success else "error")
        if success and hasattr(self.main_window_instance, 'load_works'):
            self.main_window_instance.load_works() # Refresh the works list in the main window

    def _export_csv(self):
        if not self.selected_work_id:
            show_toast(self, "Please select a Work first.", "error")
            return

        file_path = self.export_file_path.get()
        if not file_path:
            show_toast(self, "Please select a location to save the CSV file.", "warning")
            return
        
        if not file_path.lower().endswith('.csv'):
            file_path += ".csv" # Ensure correct extension

        success, message = self.schedule_item_bulk_manager.export_schedule_items_to_csv(file_path, self.selected_work_id)
        show_toast(self, message, "success" if success else "error")
