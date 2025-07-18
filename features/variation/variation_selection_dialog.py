import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from database import db_manager
from utils import helpers as utils_helpers
from features.variation.variation_data_exporter import export_variation_data_to_excel
from features.price_variation.price_variation_exporter import export_price_variation_data_to_excel
from datetime import datetime

class VariationReportSelectionDialog(tk.Toplevel):
    def __init__(self, parent, work_id):
        super().__init__(parent)
        self.parent = parent
        self.work_id = work_id
        self.work_details = db_manager.get_work_by_id(self.work_id)
        self.firm_names = db_manager.get_unique_firm_names_by_work_id(self.work_id)

        self.title("Select Variation Report Options")
        self.transient(parent)
        self.grab_set()

        self.report_type_var = tk.StringVar(self, "standard")
        self.selected_firm_var = tk.StringVar(self)

        self._create_widgets()

    def _create_widgets(self):
        # Report Type Selection
        report_type_frame = ttk.LabelFrame(self, text="Select Report Type", padx=10, pady=10)
        report_type_frame.pack(padx=10, pady=10, fill=tk.X)

        ttk.Radiobutton(report_type_frame, text="Standard Variation Report", variable=self.report_type_var, value="standard", command=self._toggle_firm_selection).pack(anchor=tk.W)
        ttk.Radiobutton(report_type_frame, text="Price Variation Report", variable=self.report_type_var, value="price", command=self._toggle_firm_selection).pack(anchor=tk.W)

        # Firm Selection
        self.firm_selection_frame = ttk.LabelFrame(self, text="Select Firm (for Price Variation)", padx=10, pady=10)
        self.firm_selection_frame.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(self.firm_selection_frame, text="Firm:").pack(side=tk.LEFT, padx=5)
        self.firm_combobox = ttk.Combobox(self.firm_selection_frame, textvariable=self.selected_firm_var, values=self.firm_names, state="readonly")
        self.firm_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if self.firm_names:
            self.selected_firm_var.set(self.firm_names[0])
        else:
            self.firm_combobox.set("No firms available")
            self.firm_combobox.config(state="disabled")

        self._toggle_firm_selection() # Initial state

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Generate Report", command=self._generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _toggle_firm_selection(self):
        if self.report_type_var.get() == "price":
            self.firm_combobox.config(state="readonly" if self.firm_names else "disabled")
        else:
            self.firm_combobox.config(state="disabled")

    def _generate_report(self):
        report_type = self.report_type_var.get()
        selected_firm = self.selected_firm_var.get()

        if report_type == "price" and not selected_firm:
            utils_helpers.show_toast(self, "Please select a firm for Price Variation Report.", "warning")
            return

        schedule_items = db_manager.get_schedule_items(self.work_id)

        file_name_suffix = ""
        exporter_function = None
        if report_type == "standard":
            file_name_suffix = "Variation_Report"
            exporter_function = export_variation_data_to_excel
            selected_firms_list = [] # Standard variation doesn't use firms in its export function
        elif report_type == "price":
            file_name_suffix = f"Price_Variation_Report_{selected_firm.replace(' ', '_')}"
            exporter_function = export_price_variation_data_to_excel
            selected_firms_list = [selected_firm]

        if not exporter_function:
            utils_helpers.show_toast(self, "Invalid report type selected.", "error")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{self.work_details['work_name'].replace(' ', '_')}_{file_name_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if not output_path:
            utils_helpers.show_toast(self, "Export cancelled.", "info")
            return

        success, message = exporter_function(self.work_details, schedule_items, output_path, selected_firms_list)
        if success:
            utils_helpers.show_toast(self.parent, f"{file_name_suffix.replace('_', ' ')} exported successfully: {output_path}", "success")
            self.destroy()
        else:
            utils_helpers.show_toast(self.parent, f"Error exporting {file_name_suffix.replace('_', ' ')}: {message}", "error")

