import tkinter as tk
from tkinter import ttk
from database import db_manager
from utils.helpers import validate_numeric_input
from features.template_engine.date_picker_widget import DatePickerWidget

class WorkDetailsExtensionTab(ttk.Frame):
    def __init__(self, notebook, parent_app, work_data_var, is_new_work_var):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.work_data_var = work_data_var
        self.is_new_work_var = is_new_work_var

        self.justification_var = tk.StringVar()
        self.section_var = tk.StringVar()
        self.work_type_var = tk.StringVar()
        self.file_no_var = tk.StringVar()
        self.estimate_no_var = tk.StringVar()
        self.tender_cost_var = tk.StringVar()
        self.tender_opening_date_var = tk.StringVar()

        self.vcmd_numeric = self.parent_app.window.register(validate_numeric_input)

        self._create_widgets()
        self._bind_data()
        self._load_section_options()

    def _create_widgets(self):
        # Justification (Long Text)
        ttk.Label(self, text="Justification:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.justification_text = tk.Text(self, wrap='word', height=5)
        self.justification_text.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.justification_text.bind("<KeyRelease>", lambda e: self._update_work_data('justification', self.justification_text.get("1.0", tk.END).strip()))

        # Section (Combobox with dynamic options)
        ttk.Label(self, text="Section:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.section_combobox = ttk.Combobox(self, textvariable=self.section_var)
        self.section_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.section_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_work_data('section', self.section_var.get()))
        self.section_combobox.bind("<KeyRelease>", lambda e: self._update_work_data('section', self.section_var.get()))

        # Type (Combobox)
        ttk.Label(self, text="Type:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.work_type_combobox = ttk.Combobox(self, textvariable=self.work_type_var, state="readonly")
        self.work_type_combobox['values'] = ["On Quotation (M&P Below Lacks)", "RSP ITEM", "Service Contract", "DRM Power"]
        self.work_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.work_type_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_work_data('work_type', self.work_type_var.get()))

        # File No.
        ttk.Label(self, text="File No.:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.file_no_entry = ttk.Entry(self, textvariable=self.file_no_var)
        self.file_no_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.file_no_var.trace_add("write", lambda *args: self._update_work_data('file_no', self.file_no_var.get()))

        # Estimate No.
        ttk.Label(self, text="Estimate No.:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.estimate_no_entry = ttk.Entry(self, textvariable=self.estimate_no_var)
        self.estimate_no_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.estimate_no_var.trace_add("write", lambda *args: self._update_work_data('estimate_no', self.estimate_no_var.get()))

        # Tender Cost
        ttk.Label(self, text="Tender Cost:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.tender_cost_entry = ttk.Entry(self, textvariable=self.tender_cost_var, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.tender_cost_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.tender_cost_var.trace_add("write", lambda *args: self._update_work_data('tender_cost', self.tender_cost_var.get()))

        # Tender Opening Date
        ttk.Label(self, text="Tender Opening Date:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.tender_opening_date_picker = DatePickerWidget(self, self.tender_opening_date_var)
        self.tender_opening_date_picker.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        self.tender_opening_date_var.trace_add("write", lambda *args: self._update_work_data('tender_opening_date', self.tender_opening_date_var.get()))


        self.grid_columnconfigure(1, weight=1)

    def _bind_data(self):
        # Load data from work_data_var to UI
        self.justification_text.delete("1.0", tk.END)
        self.justification_text.insert("1.0", str(self.work_data_var.get('justification', '')))
        self.section_var.set(self.work_data_var.get('section', ''))
        self.work_type_var.set(self.work_data_var.get('work_type', ''))
        self.file_no_var.set(self.work_data_var.get('file_no', ''))
        self.estimate_no_var.set(self.work_data_var.get('estimate_no', ''))
        self.tender_cost_var.set(self.work_data_var.get('tender_cost', ''))
        self.tender_opening_date_var.set(self.work_data_var.get('tender_opening_date', ''))

    def _update_work_data(self, key, value):
        self.work_data_var[key] = value

    def load_work_data(self, work_data):
        self.work_data_var.update(work_data)
        self._bind_data()
        self._load_section_options() # Reload section options when work data is loaded

    def _load_section_options(self):
        unique_sections = db_manager.get_all_unique_sections()
        self.section_combobox['values'] = unique_sections

    def get_work_data(self):
        return {
            'justification': self.justification_text.get("1.0", tk.END).strip(),
            'section': self.section_var.get(),
            'work_type': self.work_type_var.get(),
            'file_no': self.file_no_var.get(),
            'estimate_no': self.estimate_no_var.get(),
            'tender_cost': self.tender_cost_var.get(),
            'tender_opening_date': self.tender_opening_date_var.get()
        }