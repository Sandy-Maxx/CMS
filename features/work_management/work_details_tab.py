import tkinter as tk
from tkinter import ttk, messagebox
from database import db_manager
from utils import helpers as utils_helpers
from utils.helpers import load_icon

class WorkDetailsTab(ttk.Frame):
    def __init__(self, notebook, parent_app, work_data_dict, is_new_work_var, status_label_ref, notebook_ref, schedule_items_tab_ref, firm_rates_summary_tab_ref, populate_reference_firm_combobox_callback):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.work_data_dict = work_data_dict
        self.is_new_work_var = is_new_work_var
        self.status_label = status_label_ref
        self.notebook = notebook_ref
        self.schedule_items_tab = schedule_items_tab_ref
        self.firm_rates_summary_tab = firm_rates_summary_tab_ref
        self.populate_reference_firm_combobox_callback = populate_reference_firm_combobox_callback
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text="Work Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.work_name_entry = ttk.Entry(self, width=50)
        self.work_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.description_text = tk.Text(self, wrap='word', height=5)
        self.description_text.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.grid_columnconfigure(1, weight=1)
        self.save_icon = load_icon("save")
        self.save_button = ttk.Button(self, image=self.save_icon, compound=tk.LEFT, command=self._save_work_details, style='Primary.TButton')
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.save_button_text = "Save Work Details"
        self.save_button.bind("<Enter>", lambda e: self.save_button.config(text=self.save_button_text))
        self.save_button.bind("<Leave>", lambda e: self.save_button.config(text=""))

    def _save_work_details(self):
        work_name = self.work_name_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        if not work_name:
            utils_helpers.show_toast(self, "Work Name cannot be empty!", "error")
            self.status_label.config(text="Save failed: Work Name required.")
            return
        current_work_id = self.work_data_dict['work_id']
        is_new_work = self.is_new_work_var.get()
        
        justification = self.work_data_dict.get('justification')
        section = self.work_data_dict.get('section')
        work_type = self.work_data_dict.get('work_type')
        file_no = self.work_data_dict.get('file_no')
        estimate_no = self.work_data_dict.get('estimate_no')
        tender_cost = self.work_data_dict.get('tender_cost')

        if is_new_work:
            new_work_id = db_manager.add_work(work_name, description, justification, section, work_type, file_no, estimate_no, tender_cost)
            if new_work_id:
                self.work_data_dict['work_id'] = new_work_id
                self.is_new_work_var.set(False)
                self.parent_app.window.title(f"Edit Work Details (ID: {new_work_id})")
                utils_helpers.show_toast(self.parent_app.window, f"Work '{work_name}' created successfully! You can now add schedule items.", "success")
                self.status_label.config(text=f"Work '{work_name}' saved. Add schedule items.")
                self.notebook.select(self.schedule_items_tab)
                self.populate_reference_firm_combobox_callback()
                if self.firm_rates_summary_tab:
                    self.firm_rates_summary_tab.work_id = new_work_id
                    self.firm_rates_summary_tab.load_data()
            else:
                utils_helpers.show_toast(self.parent_app.window, "Failed to create new work.", "error")
                self.status_label.config(text="Save failed: Database error or name already exists.")
        else:
            if db_manager.update_work(current_work_id, work_name, description, justification, section, work_type, file_no, estimate_no, tender_cost):
                utils_helpers.show_toast(self.parent_app.window, f"Work '{work_name}' updated successfully!", "success")
                self.status_label.config(text=f"Work '{work_name}' updated.")
            else:
                utils_helpers.show_toast(self.parent_app.window, "Failed to update work.", "error")
                self.status_label.config(text="Save failed: Database error or name already exists.")

    def load_work_data(self, work_data):
        self.work_data_dict.update(work_data) # Update the shared dictionary
        self.work_name_entry.delete(0, tk.END)
        self.work_name_entry.insert(0, self.work_data_dict['work_name'])
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", self.work_data_dict['description'])
        self.status_label.config(text=f"Loaded work: {self.work_data_dict['work_name']}")