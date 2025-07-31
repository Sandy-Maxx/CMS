import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .bulk_io_manager import BulkIOManager
from .schedule_item_bulk_dialog import ScheduleItemBulkIODialog
from utils.helpers import show_toast

class BulkIODialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bulk Import/Export Works")
        self.parent = parent
        self.bulk_io_manager = BulkIOManager()
        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20)

        # Import Section (Works)
        import_works_frame = ttk.LabelFrame(main_frame, text="Import Works")
        import_works_frame.pack(pady=10, fill=tk.X)

        ttk.Label(import_works_frame, text="Select file to import:").pack(pady=5)
        self.import_file_path = ttk.Entry(import_works_frame, width=50)
        self.import_file_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(import_works_frame, text="Browse", command=self._browse_import_file).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(import_works_frame, text="Import Excel", command=self._import_excel).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(import_works_frame, text="Import CSV", command=self._import_csv).pack(side=tk.LEFT, padx=5, pady=5)

        # Export Section (Works)
        export_works_frame = ttk.LabelFrame(main_frame, text="Export Works")
        export_works_frame.pack(pady=10, fill=tk.X)

        ttk.Label(export_works_frame, text="Select export location:").pack(pady=5)
        self.export_file_path = ttk.Entry(export_works_frame, width=50)
        self.export_file_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(export_works_frame, text="Browse", command=self._browse_export_location).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(export_works_frame, text="Export Excel", command=self._export_excel).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(export_works_frame, text="Export CSV", command=self._export_csv).pack(side=tk.LEFT, padx=5, pady=5)

        # Schedule Item Bulk IO Button
        schedule_item_button = ttk.Button(main_frame, text="Manage Schedule Items (Bulk)", command=self._open_schedule_item_bulk_io_dialog)
        schedule_item_button.pack(pady=10)

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
        file_path = self.import_file_path.get()
        if not file_path:
            show_toast(self, "Please select an Excel file to import.", "warning")
            return
        
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            show_toast(self, "Selected file is not an Excel file.", "error")
            return

        success, message = self.bulk_io_manager.import_works_from_excel(file_path)
        show_toast(self, message, "success" if success else "error")
        if success and hasattr(self.parent, 'load_works'):
            self.parent.load_works() # Refresh the works list in the main window

    def _export_excel(self):
        file_path = self.export_file_path.get()
        if not file_path:
            show_toast(self, "Please select a location to save the Excel file.", "warning")
            return
        
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            file_path += ".xlsx" # Ensure correct extension

        success, message = self.bulk_io_manager.export_works_to_excel(file_path)
        show_toast(self, message, "success" if success else "error")

    def _import_csv(self):
        file_path = self.import_file_path.get()
        if not file_path:
            show_toast(self, "Please select a CSV file to import.", "warning")
            return
        
        if not file_path.lower().endswith('.csv'):
            show_toast(self, "Selected file is not a CSV file.", "error")
            return

        success, message = self.bulk_io_manager.import_works_from_csv(file_path)
        show_toast(self, message, "success" if success else "error")
        if success and hasattr(self.parent, 'load_works'):
            self.parent.load_works() # Refresh the works list in the main window

    def _export_csv(self):
        file_path = self.export_file_path.get()
        if not file_path:
            show_toast(self, "Please select a location to save the CSV file.", "warning")
            return
        
        if not file_path.lower().endswith('.csv'):
            file_path += ".csv" # Ensure correct extension

        success, message = self.bulk_io_manager.export_works_to_csv(file_path)
        show_toast(self, message, "success" if success else "error")

    def _open_schedule_item_bulk_io_dialog(self):
        ScheduleItemBulkIODialog(self, self.parent)