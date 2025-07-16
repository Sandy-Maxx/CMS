import tkinter as tk
from tkinter import ttk
from database.db_manager import get_work_by_id, get_all_unique_firm_names
from utils.helpers import show_toast, validate_numeric_input
from utils.styles import configure_styles
from .work_details_tab import WorkDetailsTab
from .schedule_items_tab import ScheduleItemsTab
from .individual_firm_rates_tab import IndividualFirmRatesTab

class WorkDetailsEditor:
    def __init__(self, parent, work_id, callback):
        self.work_id = work_id
        self.callback = callback
        self.window = tk.Toplevel(parent)
        self.window.title(f"{'New' if not work_id else 'Edit'} Work Details (ID: {work_id or 'New'})")
        configure_styles()
        
        self.work_id_var = tk.StringVar(value=str(work_id) if work_id else "")
        self.is_new_work_var = tk.BooleanVar(value=not work_id)
        self.reference_firm_var = tk.StringVar()
        self.vcmd_numeric = self.window.register(validate_numeric_input)
        
        self.status_label = ttk.Label(self.window, text="Ready", style="Status.TLabel")
        self.status_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self._initialization_complete = False

        self.schedule_items_tab = ScheduleItemsTab(
            self.notebook, self, self.work_id_var, self.reference_firm_var,
            self.vcmd_numeric, self.load_firm_rates, self.update_schedule_item_display_costs,
            self.populate_reference_firm_combobox
        )
        self.firm_rates_tab = IndividualFirmRatesTab(
            self.notebook, self, self.vcmd_numeric, self.firm_rates_tab_load_firm_rates,
            self.update_schedule_item_display_costs
        )
        self.work_details_tab = WorkDetailsTab(
            self.notebook, self, self.work_id_var, self.is_new_work_var, self.status_label,
            self.notebook, self.schedule_items_tab, None, self.populate_reference_firm_combobox
        )
        
        self.notebook.add(self.work_details_tab, text="Work Details")
        self.notebook.add(self.schedule_items_tab, text="Schedule Items")
        self.notebook.add(self.firm_rates_tab, text="Individual Firm Rates")
        
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.populate_reference_firm_combobox()
        
        if work_id:
            self.load_work_data()
        
        self._initialization_complete = True

        self.window.transient(parent)
        self.window.grab_set()
    
    def load_work_data(self):
        work_data = get_work_by_id(self.work_id)
        if work_data:
            self.work_details_tab.load_work_data(work_data)
            self.schedule_items_tab._load_schedule_items()
    
    def load_firm_rates(self, item_id, item_name):
        self.firm_rates_tab.load_firm_rates(item_id, item_name)
    
    def firm_rates_tab_load_firm_rates(self, item_id, item_name):
        self.firm_rates_tab.load_firm_rates(item_id, item_name)
    
    def update_schedule_item_display_costs(self):
        if not self._initialization_complete:
            return
        self.schedule_items_tab._load_schedule_items()
    
    def populate_reference_firm_combobox(self):
        firms = get_all_unique_firm_names()
        self.schedule_items_tab.reference_firm_combobox['values'] = firms
        if firms and not self.reference_firm_var.get():
            self.reference_firm_var.set(firms[0])
        elif not firms:
            self.reference_firm_var.set("")