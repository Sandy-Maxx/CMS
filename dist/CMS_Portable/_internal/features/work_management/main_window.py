import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon
from .work_editor import WorkDetailsEditor
from .work_search_bar import WorkSearchBar
from features.excel_export.excel_exporter import export_work_to_excel
from features.variation.Variation_report import VariationReportDialog
from features.vitiation.Vitiation_report import VitiationReportDialog
from features.price_variation.price_variation_exporter import export_price_variation_data_to_excel
from features.comparison.comparison_exporter import ComparisonExporter
from features.work_management.single_firm_export.single_firm_exporter import SingleFirmExporter
from datetime import datetime
from features.template_engine.template_engine_tab import TemplateEngineTab
# from features.pdf_tools.pdf_tool_tab import PdfToolTab  # Temporarily disabled due to PyMuPDF import issue
from utils.styles import set_theme
from utils.modern_components import add_mousewheel_support
from features.about_tab.about_tab import AboutTab
from features.calculation.calculation_tab import CalculationTab
from features.work_management.firm_registration.firm_registration_tab import FirmRegistrationTab
from features.AutodocGen.autodoc_manager import AutodocManager
from .bulk_io.bulk_io_dialog import BulkIODialog

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Contract Management System")
        self.root.geometry("800x600")
        self.current_theme = "light"
        set_theme(self.current_theme) # Apply the default light theme
        self._create_widgets()
        self.load_works()

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.works_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.works_frame, text="Works")

        # Frames for switching between work list and work editor
        self.works_list_frame = ttk.Frame(self.works_frame)
        self.work_editor_container_frame = ttk.Frame(self.works_frame)
        
        self.current_work_editor = None # To hold the WorkDetailsEditor instance

        self.template_engine_tab = TemplateEngineTab(self.notebook, self)
        self.notebook.add(self.template_engine_tab, text="Template Engine")

        # self.pdf_tool_tab = PdfToolTab(self.notebook, self)  # Temporarily disabled
        # self.notebook.add(self.pdf_tool_tab, text="PDF Tools")  # Temporarily disabled

        self.calculation_tab = CalculationTab(self.notebook, self)
        self.notebook.add(self.calculation_tab, text="Calculation")

        self.firm_registration_tab = FirmRegistrationTab(self.notebook)
        self.notebook.add(self.firm_registration_tab, text="Firm Registration")

        self.about_tab = AboutTab(self.notebook)
        self.notebook.add(self.about_tab, text="About")
        
        self.autodoc_manager = AutodocManager(self.root, db_manager.DATABASE_PATH)
        
        
        # Pack the frames
        self.works_list_frame.pack(fill=tk.BOTH, expand=True)
        self.work_editor_container_frame.pack(fill=tk.BOTH, expand=True)
        self.work_editor_container_frame.pack_forget() # Hide editor initially

        # Search Bar
        self.search_bar = WorkSearchBar(self.works_list_frame, self.load_works)
        self.search_bar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.works_list_frame, text="Works List", font=('Segoe UI', 11, 'bold')).pack(fill=tk.X, pady=(0, 10))
        self.works_tree = ttk.Treeview(self.works_list_frame, columns=("name", "description"), show="headings")
        self.works_tree.pack(fill=tk.BOTH, expand=True)
        self.works_tree.heading("name", text="Work Name")
        self.works_tree.heading("description", text="Description")
        self.works_tree.column("name", width=200, anchor=tk.W)
        self.works_tree.column("description", width=400, anchor=tk.W)
        vsb = ttk.Scrollbar(self.works_list_frame, orient="vertical", command=self.works_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.works_tree.configure(yscrollcommand=vsb.set)
        self.works_tree.bind("<Double-1>", self.edit_work)
        self.works_tree.bind("<Button-3>", self._show_work_context_menu)
        self.works_tree.bind("<<TreeviewSelect>>", self._on_work_selection)
        
        # Add mouse wheel scrolling support
        add_mousewheel_support(self.works_tree)

        # Context menu icons
        self.edit_icon = load_icon("edit")
        self.delete_icon = load_icon("delete")
        self.report_icon = load_icon("report")
        self.compare_icon = load_icon("compare")

        button_frame = ttk.Frame(self.works_list_frame)
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

        self.bulk_io_icon = load_icon("browse")
        self.bulk_io_button = ttk.Button(button_frame, image=self.bulk_io_icon, compound=tk.LEFT, command=self._open_bulk_io_dialog, style='Secondary.TButton')
        self.bulk_io_button.pack(side=tk.LEFT, padx=5)
        self.bulk_io_button_text = "Bulk Import/Export"
        self.bulk_io_button.bind("<Enter>", lambda e: self.bulk_io_button.config(text=self.bulk_io_button_text))
        self.bulk_io_button.bind("<Leave>", lambda e: self.bulk_io_button.config(text=""))

        self.backup_icon = load_icon("save") # Assuming a 'save.png' icon exists or is appropriate
        self.backup_button = ttk.Button(button_frame, image=self.backup_icon, compound=tk.LEFT, command=self._backup_database, style='Success.TButton')
        self.backup_button.pack(side=tk.LEFT, padx=5)
        self.backup_button_text = "Backup Database"
        self.backup_button.bind("<Enter>", lambda e: self.backup_button.config(text=self.backup_button_text))
        self.backup_button.bind("<Leave>", lambda e: self.backup_button.config(text=""))

        self.restore_icon = load_icon("rotate") # Using a rotate icon for restore
        self.restore_button = ttk.Button(button_frame, image=self.restore_icon, compound=tk.LEFT, command=self._restore_database, style='Warning.TButton')
        self.restore_button.pack(side=tk.LEFT, padx=5)
        self.restore_button_text = "Restore Database"
        self.restore_button.bind("<Enter>", lambda e: self.restore_button.config(text=self.restore_button_text))
        self.restore_button.bind("<Leave>", lambda e: self.restore_button.config(text=""))

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _show_work_list_view(self):
        self.work_editor_container_frame.pack_forget()
        self.works_list_frame.pack(fill=tk.BOTH, expand=True)
        self.load_works() # Refresh the list when returning to it

    def _show_work_editor_view(self, work_id=None):
        self.works_list_frame.pack_forget()
        self.work_editor_container_frame.pack(fill=tk.BOTH, expand=True)

        # Clear previous editor if any
        for widget in self.work_editor_container_frame.winfo_children():
            widget.destroy()
        
        # Create and pack the new WorkDetailsEditor
        self.current_work_editor = WorkDetailsEditor(self.work_editor_container_frame, self, work_id, self.root)
        self.current_work_editor.pack(fill=tk.BOTH, expand=True)
        self.template_engine_tab.set_work_id(work_id) # Update the TemplateEngineTab with the current work_id

    def _show_work_context_menu(self, event):
        # Select item on right-click
        item_id = self.works_tree.identify_row(event.y)
        if item_id:
            self.works_tree.selection_set(item_id)
            self.works_tree.focus(item_id)
            # Update template_engine_tab with selected work_id
            work_id = int(item_id)
            self.template_engine_tab.set_work_id(work_id)
            
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Export Variation Report", image=self.report_icon, compound=tk.LEFT, command=self._export_variation_report)
            context_menu.add_command(label="Export Vitiation Report", image=self.report_icon, compound=tk.LEFT, command=self._export_vitiation_report)
            context_menu.add_command(label="Export Comparison Report", image=self.compare_icon, compound=tk.LEFT, command=self._export_comparison_report)
            context_menu.add_command(label="Export Single Firm Report", image=self.report_icon, compound=tk.LEFT, command=self._export_single_firm_report)
            context_menu.add_command(label="Export Price Variation Report", image=self.report_icon, compound=tk.LEFT, command=self._export_price_variation_report)
            context_menu.add_command(label="Export Estimate Report", image=self.report_icon, compound=tk.LEFT, command=self._export_estimate_report)
            context_menu.add_separator()
            context_menu.add_command(label="Letters", image=self.report_icon, compound=tk.LEFT, command=lambda: self.autodoc_manager.generate_document(work_id, "Letters"))
            context_menu.add_command(label="Office Notes", image=self.report_icon, compound=tk.LEFT, command=lambda: self.autodoc_manager.generate_document(work_id, "OfficeNotes"))
            
            
            context_menu.add_separator()
            context_menu.add_command(label="Delete Work", image=self.delete_icon, compound=tk.LEFT, command=self._delete_work)
            context_menu.post(event.x_root, event.y_root)

    def _delete_work(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to delete.", "warning")
            return
        work_id = int(selected_item[0])
        work_name = self.works_tree.item(selected_item[0], "values")[0]

        if utils_helpers.show_confirm_dialog(self.root, f"Are you sure you want to delete work '{work_name}' and all its associated data?"):
            if db_manager.delete_work(work_id):
                utils_helpers.show_toast(self.root, f"Work '{work_name}' deleted successfully.", "success")
                self.load_works()
            else:
                utils_helpers.show_toast(self.root, f"Failed to delete work '{work_name}'.", "error")

    

    

    

    

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

    def _export_price_variation_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Price Variation Report.", "warning")
            return
        work_id = int(selected_item[0])
        work_details = db_manager.get_work_by_id(work_id)
        if not work_details:
            utils_helpers.show_toast(self.root, "Failed to retrieve work details.", "error")
            return
        schedule_items = db_manager.get_schedule_items(work_id)
        
        # Get unique firm names for the selected work
        firm_names = db_manager.get_unique_firm_names_by_work_id(work_id)
        if not firm_names:
            utils_helpers.show_toast(self.root, "No firm rates found for this work.", "info")
            return

        selected_firm, variation_name = self._ask_for_price_variation_options(firm_names, work_id)
        if not selected_firm or not variation_name:
            utils_helpers.show_toast(self.root, "Selection cancelled.", "info")
            return
        selected_firms = [selected_firm]
        
        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{work_details['work_name'].replace(' ', '_')}_Price_Variation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not output_path:
            utils_helpers.show_toast(self.root, "Export cancelled.", "info")
            return
        
        success, message = export_price_variation_data_to_excel(work_details, schedule_items, output_path, selected_firms, variation_name)
        if success:
            utils_helpers.show_toast(self.root, f"Price Variation Report exported successfully: {output_path}", "success")
        else:
            utils_helpers.show_toast(self.root, f"Error exporting Price Variation Report: {message}", "error")

    def _export_estimate_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Estimate Report.", "warning")
            return
        work_id = int(selected_item[0])
        work_details = db_manager.get_work_by_id(work_id)
        if not work_details:
            utils_helpers.show_toast(self.root, "Failed to retrieve work details.", "error")
            return

        firm_names = db_manager.get_unique_firm_names_by_work_id(work_id)
        if not firm_names:
            utils_helpers.show_toast(self.root, "No firm rates found for this work.", "info")
            return

        selected_firm = self._ask_for_firm_selection(firm_names)
        if not selected_firm:
            utils_helpers.show_toast(self.root, "Firm selection cancelled.", "info")
            return

        # Ask for estimate number, pre-filled with database value if available
        estimate_no = self._ask_for_estimate_number(work_details.get('estimate_no'))
        if estimate_no is None:  # User cancelled
            utils_helpers.show_toast(self.root, "Estimate number input cancelled.", "info")
            return

        # Call the new export_runner with work_id, selected_firm, and estimate_no
        from features.estimates.export_runner import run_export
        try:
            run_export(work_id, selected_firm, estimate_no)
            utils_helpers.show_toast(self.root, "Estimate Report generated successfully.", "success")
        except Exception as e:
            import traceback
            traceback.print_exc()
            utils_helpers.show_toast(self.root, f"Error generating Estimate Report: {e}", "error")

    def _export_comparison_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Comparison Report.", "warning")
            return
        work_id = int(selected_item[0])
        work_details = db_manager.get_work_by_id(work_id)
        if not work_details:
            utils_helpers.show_toast(self.root, "Failed to retrieve work details.", "error")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{work_details['work_name'].replace(' ', '_')}_Comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self.root, "Export cancelled.", "info")
            return
        try:
            exporter = ComparisonExporter(work_id)
            exporter.export_to_excel(file_path)
            utils_helpers.show_toast(self.root, f"Comparison report exported successfully: {file_path}", "success")
        except Exception as e:
            import traceback
            traceback.print_exc()
            utils_helpers.show_toast(self.root, f"Error exporting comparison report: {e}", "error")

    def _export_single_firm_report(self):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to generate Single Firm Report.", "warning")
            return
        work_id = int(selected_item[0])
        work_details = db_manager.get_work_by_id(work_id)
        if not work_details:
            utils_helpers.show_toast(self.root, "Failed to retrieve work details.", "error")
            return

        # Get unique firm names for the selected work
        firm_names = db_manager.get_unique_firm_names_by_work_id(work_id)
        if not firm_names:
            utils_helpers.show_toast(self.root, "No firm rates found for this work.", "info")
            return

        # Prompt user to select a firm
        selected_firm = self._ask_for_firm_selection(firm_names)
        if not selected_firm:
            utils_helpers.show_toast(self.root, "Firm selection cancelled.", "info")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{work_details['work_name'].replace(' ', '_')}_{selected_firm.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not file_path:
            utils_helpers.show_toast(self.root, "Export cancelled.", "info")
            return
        try:
            exporter = SingleFirmExporter(work_id, selected_firm)
            exporter.export_to_excel(file_path)
            utils_helpers.show_toast(self.root, f"Single firm report for {selected_firm} exported successfully: {file_path}", "success")
        except Exception as e:
            import traceback
            traceback.print_exc()
            utils_helpers.show_toast(self.root, f"Error exporting single firm report: {e}", "error")

    def _ask_for_price_variation_options(self, firm_names, work_id):
        dialog = tk.Toplevel(self.root)
        dialog.title("Price Variation Options")
        dialog.transient(self.root)
        dialog.grab_set()

        # Firm Selection
        tk.Label(dialog, text="Select a firm:").pack(padx=10, pady=5)
        firm_var = tk.StringVar(dialog)
        firm_var.set(firm_names[0] if firm_names else "")
        firm_combobox = ttk.Combobox(dialog, textvariable=firm_var, values=firm_names, state="readonly")
        firm_combobox.pack(padx=10, pady=5)

        # Variation Name Selection
        tk.Label(dialog, text="Select Variation Name:").pack(padx=10, pady=5)
        variation_names = db_manager.get_variation_names_for_work(work_id)
        if not variation_names:
            messagebox.showerror("Error", "No variations found for this work.")
            dialog.destroy()
            return None, None

        variation_name_var = tk.StringVar(dialog)
        variation_name_var.set(variation_names[0]) # Default to the first variation name
        variation_name_combobox = ttk.Combobox(dialog, textvariable=variation_name_var, values=variation_names, state="readonly")
        variation_name_combobox.pack(padx=10, pady=5)

        selected_firm = None
        selected_variation_name = None

        def on_ok():
            nonlocal selected_firm, selected_variation_name
            selected_firm = firm_var.get()
            selected_variation_name = variation_name_var.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(dialog)
        return selected_firm, selected_variation_name

    def _ask_for_firm_selection(self, firm_names):
        # This function is now deprecated and will be removed or refactored if not used elsewhere.
        # For now, it remains to avoid breaking other parts of the code that might call it.
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Firm")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Select a firm:").pack(padx=10, pady=10)
        
        firm_var = tk.StringVar(dialog)
        firm_var.set(firm_names[0] if firm_names else "") # Set initial value
        
        firm_combobox = ttk.Combobox(dialog, textvariable=firm_var, values=firm_names, state="readonly")
        firm_combobox.pack(padx=10, pady=5)

        selected_firm = None
        def on_ok():
            nonlocal selected_firm
            selected_firm = firm_var.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(dialog)
        return selected_firm

    def _ask_for_estimate_number(self, prefill_value=None):
        """Ask user to input estimate number for the report.
        
        Args:
            prefill_value: Optional value to pre-fill the entry field
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Estimate Number")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("400x180")
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Enter Estimate Number:", font=('Segoe UI', 10)).pack(padx=10, pady=10)
        
        # Show current value if available
        if prefill_value:
            current_label = tk.Label(dialog, text=f"Current: {prefill_value}", font=('Segoe UI', 9), fg='gray')
            current_label.pack(padx=10, pady=(0, 5))
        
        entry_var = tk.StringVar(dialog)
        # Pre-fill with database value if available
        if prefill_value:
            entry_var.set(prefill_value)
            
        entry = ttk.Entry(dialog, textvariable=entry_var, font=('Segoe UI', 10), width=30)
        entry.pack(padx=10, pady=5)
        entry.focus_set()  # Set focus to the entry field
        entry.select_range(0, tk.END)  # Select all text for easy replacement

        result = None
        
        def on_ok():
            nonlocal result
            estimate_no = entry_var.get().strip()
            if not estimate_no:
                messagebox.showwarning("Warning", "Please enter an estimate number.")
                return
            result = estimate_no
            dialog.destroy()

        def on_cancel():
            nonlocal result
            result = None
            dialog.destroy()

        # Handle Enter key to submit
        def on_enter(event):
            on_ok()
        
        entry.bind('<Return>', on_enter)
        dialog.bind('<Escape>', lambda e: on_cancel())

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="OK", command=on_ok, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(dialog)
        return result

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
        self._show_work_editor_view(work_id=None)

    def edit_work(self, event=None):
        selected_item = self.works_tree.selection()
        if not selected_item:
            utils_helpers.show_toast(self.root, "Please select a work to edit.", "warning")
            return
        work_id = int(selected_item[0])
        self.template_engine_tab.set_work_id(work_id) # Update the TemplateEngineTab with the current work_id
        self._show_work_editor_view(work_id=work_id)

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

    





    def _backup_database(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            initialfile=f"cms_database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
        print(f"Generated backup filename: {file_path}") # Added for debugging
        if file_path:
            success, message = db_manager.backup_database(file_path)
            utils_helpers.show_toast(self.root, message, "success" if success else "error")

    def _restore_database(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if file_path:
            if utils_helpers.show_confirm_dialog(self.root, "Restoring the database will overwrite current data. Are you sure?"):
                success, message = db_manager.restore_database(file_path)
                utils_helpers.show_toast(self.root, message, "success" if success else "error")
                if success:
                    self.load_works() # Reload data after successful restore

    def _open_bulk_io_dialog(self):
        BulkIODialog(self.root)


    def _on_work_selection(self, event):
        selected_item = self.works_tree.selection()
        if selected_item:
            work_id = int(selected_item[0])
            self.template_engine_tab.set_work_id(work_id)
        else:
            self.template_engine_tab.set_work_id(None) # Clear work_id if nothing is selected

