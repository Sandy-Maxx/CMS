import tkinter as tk
from tkinter import ttk
from database import db_manager
from utils.helpers import validate_numeric_input, show_toast
from utils.date_picker import DatePicker
from utils.modern_components import add_mousewheel_support
from utils.minimal_date_picker import MinimalDatePicker
from datetime import datetime, timedelta

class WorkDetailsExtensionTab(ttk.Frame):
    def __init__(self, notebook, parent_app, work_data_var, is_new_work_var, main_window_instance):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.work_data_var = work_data_var
        self.is_new_work_var = is_new_work_var
        self.main_window_instance = main_window_instance

        self.justification_var = tk.StringVar()
        self.section_var = tk.StringVar()
        self.work_type_var = tk.StringVar()
        self.work_type_category_var = tk.StringVar()
        self.work_type_subcategory_var = tk.StringVar()
        self.file_no_var = tk.StringVar()
        self.estimate_no_var = tk.StringVar()
        self.tender_cost_var = tk.StringVar()
        self.tender_opening_date_var = tk.StringVar()
        self.loa_no_var = tk.StringVar()
        self.loa_date_var = tk.StringVar()
        self.work_commence_date_var = tk.StringVar()
        self.admin_approval_office_note_no_var = tk.StringVar()
        self.admin_approval_date_var = tk.StringVar()

        self.concurrence_letter_no_var = tk.StringVar()
        self.concurrence_letter_dated_var = tk.StringVar()
        self.dr_dfm_eoffice_note_no_var = tk.StringVar()
        self.computer_no_var = tk.StringVar()

        self.vcmd_numeric = self.parent_app.register(validate_numeric_input)

        # Create scrollable container hierarchy
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        
        # Add mouse wheel support to scroll the canvas
        add_mousewheel_support(self.canvas, canvas=self.canvas)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create the form frame inside the canvas
        self.form_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.form_frame)
        
        # Configure scrolling
        self.form_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self._create_widgets()
        self._bind_data()
        self._load_section_options()

    def _create_widgets(self):
        # Justification (Long Text)
        ttk.Label(self.form_frame, text="Justification:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.justification_text = tk.Text(self.form_frame, wrap='word', height=5)
        self.justification_text.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.justification_text.bind("<KeyRelease>", lambda e: self._update_work_data('justification', self.justification_text.get("1.0", tk.END).strip()))
        
        # Add mouse wheel scrolling support
        add_mousewheel_support(self.justification_text)

        # Section (Combobox with dynamic options)
        ttk.Label(self.form_frame, text="Section:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.section_combobox = ttk.Combobox(self.form_frame, textvariable=self.section_var)
        self.section_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.section_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_work_data('section', self.section_var.get()))
        self.section_combobox.bind("<KeyRelease>", lambda e: self._update_work_data('section', self.section_var.get()))

        # Type of Work (Hierarchical Dropdown)
        ttk.Label(self.form_frame, text="Type of Work:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        # Create frame for hierarchical dropdown
        work_type_frame = ttk.Frame(self.form_frame)
        work_type_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # First level dropdown (Category)
        self.work_type_category_combobox = ttk.Combobox(work_type_frame, textvariable=self.work_type_category_var, state="readonly", width=15)
        self.work_type_category_combobox['values'] = ["DRM Power", "Sr.DEE Power", "HQ Power"]
        self.work_type_category_combobox.pack(side=tk.LEFT, padx=(0, 5))
        self.work_type_category_combobox.bind("<<ComboboxSelected>>", self._on_work_type_category_change)
        
        # Second level dropdown (Subcategory)
        self.work_type_subcategory_combobox = ttk.Combobox(work_type_frame, textvariable=self.work_type_subcategory_var, state="readonly", width=15)
        self.work_type_subcategory_combobox['values'] = ["M&P", "RSP", "SERVICE"]
        self.work_type_subcategory_combobox.pack(side=tk.LEFT)
        self.work_type_subcategory_combobox.bind("<<ComboboxSelected>>", self._on_work_type_subcategory_change)

        # File No.
        ttk.Label(self.form_frame, text="File No.:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.file_no_combobox = ttk.Combobox(self.form_frame, textvariable=self.file_no_var)
        self.file_no_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.file_no_combobox.bind("<KeyRelease>", lambda event: self._on_combobox_key_release(event, self.file_no_combobox, db_manager.get_all_unique_file_numbers))
        self.file_no_var.trace_add("write", lambda *args: self._update_work_data('file_no', self.file_no_var.get()))

        # Estimate No.
        ttk.Label(self.form_frame, text="Estimate No.:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.estimate_no_combobox = ttk.Combobox(self.form_frame, textvariable=self.estimate_no_var)
        self.estimate_no_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.estimate_no_combobox.bind("<KeyRelease>", lambda event: self._on_combobox_key_release(event, self.estimate_no_combobox, db_manager.get_all_unique_estimate_numbers))
        self.estimate_no_var.trace_add("write", lambda *args: self._update_work_data('estimate_no', self.estimate_no_var.get()))

        # Tender Cost
        ttk.Label(self.form_frame, text="Tender Cost:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.tender_cost_entry = ttk.Entry(self.form_frame, textvariable=self.tender_cost_var, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.tender_cost_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.tender_cost_var.trace_add("write", lambda *args: self._update_work_data('tender_cost', self.tender_cost_var.get()))

        # Tender Opening Date
        ttk.Label(self.form_frame, text="Tender Opening Date:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.tender_opening_date_picker = MinimalDatePicker(self.form_frame, textvariable=self.tender_opening_date_var)
        self.tender_opening_date_picker.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        self.tender_opening_date_var.trace_add("write", lambda *args: self._update_work_data('tender_opening_date', self.tender_opening_date_var.get()))

        # LOA No.
        ttk.Label(self.form_frame, text="LOA No.:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.loa_no_combobox = ttk.Combobox(self.form_frame, textvariable=self.loa_no_var)
        self.loa_no_combobox.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        self.loa_no_combobox.bind("<KeyRelease>", lambda event: self._on_combobox_key_release(event, self.loa_no_combobox, db_manager.get_all_unique_loa_numbers))
        self.loa_no_var.trace_add("write", lambda *args: self._update_work_data('loa_no', self.loa_no_var.get()))

        # LOA Date
        ttk.Label(self.form_frame, text="LOA Date:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.loa_date_picker = MinimalDatePicker(self.form_frame, textvariable=self.loa_date_var)
        self.loa_date_picker.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        self.loa_date_var.trace_add("write", lambda *args: self._update_work_data('loa_date', self.loa_date_var.get()))

        # Work Commence Date
        ttk.Label(self.form_frame, text="Work Commence Date:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.work_commence_date_picker = MinimalDatePicker(self.form_frame, textvariable=self.work_commence_date_var)
        self.work_commence_date_picker.grid(row=9, column=1, padx=5, pady=5, sticky="ew")
        self.work_commence_date_var.trace_add("write", lambda *args: self._update_work_data('work_commence_date', self.work_commence_date_var.get()))

        # Admin Approval Office Note No.
        ttk.Label(self.form_frame, text="Admin Approval Office Note No.:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.admin_approval_office_note_no_entry = ttk.Entry(self.form_frame, textvariable=self.admin_approval_office_note_no_var)
        self.admin_approval_office_note_no_entry.grid(row=10, column=1, padx=5, pady=5, sticky="ew")
        self.admin_approval_office_note_no_var.trace_add("write", lambda *args: self._update_work_data('admin_approval_office_note_no', self.admin_approval_office_note_no_var.get()))

        # Admin Approval Date
        ttk.Label(self.form_frame, text="Admin Approval Date:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.admin_approval_date_picker = MinimalDatePicker(self.form_frame, textvariable=self.admin_approval_date_var)
        self.admin_approval_date_picker.grid(row=11, column=1, padx=5, pady=5, sticky="ew")
        self.admin_approval_date_var.trace_add("write", lambda *args: self._update_work_data('admin_approval_date', self.admin_approval_date_var.get()))

        # Concurrence Details
        ttk.Label(self.form_frame, text="Concurrence Letter No.:").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.concurrence_letter_no_entry = ttk.Entry(self.form_frame, textvariable=self.concurrence_letter_no_var)
        self.concurrence_letter_no_entry.grid(row=12, column=1, padx=5, pady=5, sticky="ew")
        self.concurrence_letter_no_var.trace_add("write", lambda *args: self._update_work_data('concurrence_letter_no', self.concurrence_letter_no_var.get()))

        ttk.Label(self.form_frame, text="Concurrence Letter Dated:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.concurrence_letter_dated_picker = MinimalDatePicker(self.form_frame, textvariable=self.concurrence_letter_dated_var)
        self.concurrence_letter_dated_picker.grid(row=13, column=1, padx=5, pady=5, sticky="ew")
        self.concurrence_letter_dated_var.trace_add("write", lambda *args: self._update_work_data('concurrence_letter_dated', self.concurrence_letter_dated_var.get()))

        ttk.Label(self.form_frame, text="Dr.DFM eOffice Note No.:").grid(row=14, column=0, padx=5, pady=5, sticky="w")
        self.dr_dfm_eoffice_note_no_entry = ttk.Entry(self.form_frame, textvariable=self.dr_dfm_eoffice_note_no_var)
        self.dr_dfm_eoffice_note_no_entry.grid(row=14, column=1, padx=5, pady=5, sticky="ew")
        self.dr_dfm_eoffice_note_no_var.trace_add("write", lambda *args: self._update_work_data('dr_dfm_eoffice_note_no', self.dr_dfm_eoffice_note_no_var.get()))

        ttk.Label(self.form_frame, text="Computer No.:").grid(row=15, column=0, padx=5, pady=5, sticky="w")
        self.computer_no_entry = ttk.Entry(self.form_frame, textvariable=self.computer_no_var)
        self.computer_no_entry.grid(row=15, column=1, padx=5, pady=5, sticky="ew")
        self.computer_no_var.trace_add("write", lambda *args: self._update_work_data('computer_no', self.computer_no_var.get()))

        save_button = ttk.Button(self.form_frame, text="Save Additional Details", command=self._save_data)
        save_button.grid(row=16, column=0, columnspan=2, pady=10)

        self.form_frame.grid_columnconfigure(1, weight=1)

    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Update the canvas window width when canvas size changes"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _bind_data(self):
        # Load data from work_data_var to UI
        self.justification_text.delete("1.0", tk.END)
        self.justification_text.insert("1.0", str(self.work_data_var.get('justification', '')))
        self.section_var.set(self.work_data_var.get('section', ''))
        self.work_type_var.set(self.work_data_var.get('work_type', ''))
        self.work_type_category_var.set(self.work_data_var.get('work_type_category', ''))
        self.work_type_subcategory_var.set(self.work_data_var.get('work_type_subcategory', ''))
        self.file_no_var.set(self.work_data_var.get('file_no', ''))
        self.estimate_no_var.set(self.work_data_var.get('estimate_no', ''))
        self.tender_cost_var.set(self.work_data_var.get('tender_cost', ''))
        self.tender_opening_date_var.set(self.work_data_var.get('tender_opening_date', ''))
        self.loa_no_var.set(self.work_data_var.get('loa_no', ''))
        self.loa_date_var.set(self.work_data_var.get('loa_date', ''))
        self.work_commence_date_var.set(self.work_data_var.get('work_commence_date', ''))
        self.admin_approval_office_note_no_var.set(self.work_data_var.get('admin_approval_office_note_no', ''))
        self.admin_approval_date_var.set(self.work_data_var.get('admin_approval_date', ''))
        self.concurrence_letter_no_var.set(self.work_data_var.get('concurrence_letter_no', ''))
        self.concurrence_letter_dated_var.set(self.work_data_var.get('concurrence_letter_dated', ''))
        self.dr_dfm_eoffice_note_no_var.set(self.work_data_var.get('dr_dfm_eoffice_note_no', ''))
        self.computer_no_var.set(self.work_data_var.get('computer_no', ''))

        # Populate comboboxes with all unique values for autosuggestion
        self.file_no_combobox['values'] = db_manager.get_all_unique_file_numbers()
        self.estimate_no_combobox['values'] = db_manager.get_all_unique_estimate_numbers()
        self.loa_no_combobox['values'] = db_manager.get_all_unique_loa_numbers()

    def _update_work_data(self, key, value):
        self.work_data_var[key] = value

    def load_work_data(self, work_data):
        self.work_data_var.update(work_data)
        self._bind_data()
        self._load_section_options() # Reload section options when work data is loaded

    def _load_section_options(self):
        unique_sections = db_manager.get_all_unique_sections()
        self.section_combobox['values'] = unique_sections

    def _on_work_type_category_change(self, event=None):
        """Handle first level dropdown selection"""
        category = self.work_type_category_var.get()
        self._update_work_data('work_type_category', category)
        # Update the combined work_type field
        self._update_combined_work_type()
    
    def _on_work_type_subcategory_change(self, event=None):
        """Handle second level dropdown selection"""
        subcategory = self.work_type_subcategory_var.get()
        self._update_work_data('work_type_subcategory', subcategory)
        # Update the combined work_type field
        self._update_combined_work_type()
    
    def _update_combined_work_type(self):
        """Update the legacy work_type field based on category and subcategory"""
        category = self.work_type_category_var.get()
        subcategory = self.work_type_subcategory_var.get()
        if category and subcategory:
            combined = f"{category} - {subcategory}"
            self.work_type_var.set(combined)
            self._update_work_data('work_type', combined)

    def _on_combobox_key_release(self, event, combobox_widget, get_all_function_ref):
        search_text = combobox_widget.get().lower()
        if search_text == '':
            combobox_widget['values'] = get_all_function_ref()
        else:
            filtered_values = [item for item in get_all_function_ref() if search_text in item.lower()]
            combobox_widget['values'] = filtered_values

    def _scroll_date(self, event, date_var):
        try:
            current_date = datetime.strptime(date_var.get(), "%d-%m-%Y")
        except ValueError:
            current_date = datetime.now()

        if event.delta > 0:  # Scroll up
            new_date = current_date + timedelta(days=1)
        else:  # Scroll down
            new_date = current_date - timedelta(days=1)

        date_var.set(new_date.strftime("%d-%m-%Y"))

    def _save_data(self):
        work_id = self.work_data_var.get('work_id')
        if not work_id:
            show_toast(self, "Cannot save: Work ID is missing.", "error")
            return

        work_name = self.work_data_var.get('work_name')
        description = self.work_data_var.get('description')
        justification = self.justification_text.get("1.0", tk.END).strip()
        section = self.section_var.get()
        work_type = self.work_type_var.get()
        file_no = self.file_no_var.get()
        estimate_no = self.estimate_no_var.get()
        tender_cost = self.tender_cost_var.get()
        tender_opening_date = self.tender_opening_date_var.get()
        loa_no = self.loa_no_var.get()
        loa_date = self.loa_date_var.get()
        work_commence_date = self.work_commence_date_var.get()
        admin_approval_office_note_no = self.admin_approval_office_note_no_var.get()
        admin_approval_date = self.admin_approval_date_var.get()
        work_type_category = self.work_type_category_var.get()
        work_type_subcategory = self.work_type_subcategory_var.get()
        concurrence_letter_no = self.concurrence_letter_no_var.get()
        concurrence_letter_dated = self.concurrence_letter_dated_var.get()
        dr_dfm_eoffice_note_no = self.dr_dfm_eoffice_note_no_var.get()
        computer_no = self.computer_no_var.get()

        try:
            db_manager.update_work(
                work_id, work_name, description, justification, section, work_type,
                file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date,
                admin_approval_office_note_no, admin_approval_date, work_type_category, work_type_subcategory,
                concurrence_letter_no, concurrence_letter_dated, dr_dfm_eoffice_note_no, computer_no
            )
            show_toast(self, "Additional details saved successfully.", "success")
        except Exception as e:
            show_toast(self, f"Error saving additional details: {e}", "error")

    def get_work_data(self):
        return {
            'justification': self.justification_text.get("1.0", tk.END).strip(),
            'section': self.section_var.get(),
            'work_type': self.work_type_var.get(),
            'file_no': self.file_no_var.get(),
            'estimate_no': self.estimate_no_var.get(),
            'tender_cost': self.tender_cost_var.get(),
            'tender_opening_date': self.tender_opening_date_var.get(),
            'loa_no': self.loa_no_var.get(),
            'loa_date': self.loa_date_var.get(),
            'work_commence_date': self.work_commence_date_var.get()
        }