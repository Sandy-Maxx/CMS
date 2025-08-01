import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from features.firm_documents.firm_documents_manager import (
    add_firm_document, get_firm_documents, update_firm_document, delete_firm_document, get_firm_document_by_work_and_firm_name
)
from database import db_manager
from utils.helpers import show_toast, validate_numeric_input
from utils.date_picker import DatePicker
from utils.minimal_date_picker import MinimalDatePicker
from datetime import datetime

class FirmDocumentsTab(ttk.Frame):
    def __init__(self, parent_notebook, work_id_var, main_window_instance):
        super().__init__(parent_notebook)
        self.work_id_var = work_id_var
        self.work_id_var.trace("w", self._on_work_id_change)
        self.main_window_instance = main_window_instance

        self.vcmd_numeric = self.register(validate_numeric_input)
        self.selected_doc_id = None # To store the ID of the document being edited
        self.pg_vetted_on_placeholder = "DD-MM-YYYY"  # Initialize placeholder

        self._create_widgets()
        self.load_firm_documents()

    def _create_widgets(self):
        # Create form frame to hold all widgets
        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.form_frame, text="Add/Edit Firm Document")
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        # Firm Name
        ttk.Label(input_frame, text="Firm Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.firm_name_var = tk.StringVar()
        self.firm_name_combobox = ttk.Combobox(input_frame, textvariable=self.firm_name_var)
        self.firm_name_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.firm_name_combobox.bind("<KeyRelease>", self._on_firm_name_key_release)
        self.firm_name_combobox.bind("<<ComboboxSelected>>", self._on_firm_selected)

        # PG Submitted Checkbox
        self.pg_submitted_var = tk.BooleanVar(value=False)
        self.pg_submitted_checkbutton = ttk.Checkbutton(input_frame, text="PG Submitted", variable=self.pg_submitted_var, command=self._toggle_pg_fields)
        self.pg_submitted_checkbutton.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # PG Type
        ttk.Label(input_frame, text="PG Type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.pg_type_var = tk.StringVar()
        self.pg_type_combobox = ttk.Combobox(input_frame, textvariable=self.pg_type_var, values=[
            "G – Performance Guarantee", "BG – Bank Guarantee", "PBG – Performance Bank Guarantee",
            "ABG – Advance Bank Guarantee", "RBG – Retention Bank Guarantee", "MBG – Mobilization Bank Guarantee",
            "FDR – Fixed Deposit Receipt", "SD – Security Deposit", "EMD – Earnest Money Deposit",
            "PS – Performance Security", "IB – Insurance Bond", "SB – Surety Bond"
        ])
        self.pg_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        self.pg_type_combobox.bind("<<ComboboxSelected>>", self._toggle_pg_fields)

        # PG No
        ttk.Label(input_frame, text="PG No.:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.pg_no_entry = ttk.Entry(input_frame)
        self.pg_no_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.EW)

        # PG Amount
        ttk.Label(input_frame, text="PG Amount:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.pg_amount_entry = ttk.Entry(input_frame, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.pg_amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        # PG Vetted On
        ttk.Label(input_frame, text="PG Vetted On:").grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.pg_vetted_on_var = tk.StringVar()
        self.pg_vetted_on_picker = MinimalDatePicker(input_frame, textvariable=self.pg_vetted_on_var)
        self.pg_vetted_on_picker.grid(row=3, column=3, padx=5, pady=5, sticky=tk.EW)

        # Bank Name
        ttk.Label(input_frame, text="Bank Name:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.bank_name_entry = ttk.Entry(input_frame)
        self.bank_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

        # Bank Address
        ttk.Label(input_frame, text="Bank Address:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.bank_address_entry = ttk.Entry(input_frame)
        self.bank_address_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.EW)
        self._toggle_pg_fields()

        # Indemnity Bond Submitted Checkbox
        self.indemnity_bond_submitted_var = tk.BooleanVar(value=False)
        self.indemnity_bond_submitted_checkbutton = ttk.Checkbutton(input_frame, text="Indemnity Bond Submitted", variable=self.indemnity_bond_submitted_var, command=self._toggle_indemnity_bond_fields)
        self.indemnity_bond_submitted_checkbutton.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        # Indemnity Bond Details
        ttk.Label(input_frame, text="Indemnity Bond Details:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.indemnity_bond_details_entry = ttk.Entry(input_frame)
        self.indemnity_bond_details_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.EW)

        # IB Vetted On
        ttk.Label(input_frame, text="IB Vetted On:").grid(row=7, column=2, padx=5, pady=5, sticky=tk.W)
        self.ib_vetted_on_var = tk.StringVar()
        self.ib_vetted_on_picker = MinimalDatePicker(input_frame, textvariable=self.ib_vetted_on_var)
        self.ib_vetted_on_picker.grid(row=7, column=3, padx=5, pady=5, sticky=tk.EW)
        self._toggle_indemnity_bond_fields()

        

        # Other Docs Details
        ttk.Label(input_frame, text="Other Docs Details:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.other_docs_details_entry = ttk.Entry(input_frame)
        self.other_docs_details_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.EW)

        # Submission Date
        ttk.Label(input_frame, text="Submission Date:").grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.submission_date_var = tk.StringVar()
        self.submission_date_var.set(datetime.now().strftime("%d-%m-%Y"))
        self.submission_date_picker = MinimalDatePicker(input_frame, textvariable=self.submission_date_var)
        self.submission_date_picker.grid(row=10, column=1, padx=5, pady=5, sticky=tk.EW)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=10)
        self.add_button = ttk.Button(button_frame, text="Add Document", command=self._add_document)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.update_button = ttk.Button(button_frame, text="Update Document", command=self._update_document, state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_form)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Documents List
        documents_frame = ttk.LabelFrame(self.form_frame, text="Firm Documents")
        documents_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.documents_tree = ttk.Treeview(documents_frame, columns=(
            "firm_name", "pg_submitted", "pg_type", "pg_no", "pg_amount", "bank_name", "bank_address", "pg_vetted_on",
            "indemnity_bond_submitted", "indemnity_bond_details", "ib_vetted_on", "other_docs_details", "submission_date"
        ), show="headings")
        self.documents_tree.pack(fill=tk.BOTH, expand=True)

        self.documents_tree.heading("firm_name", text="Firm Name")
        self.documents_tree.heading("pg_submitted", text="PG Submitted")
        self.documents_tree.heading("pg_type", text="PG Type")
        self.documents_tree.heading("pg_no", text="PG No.")
        self.documents_tree.heading("pg_amount", text="PG Amount")
        self.documents_tree.heading("bank_name", text="Bank Name")
        self.documents_tree.heading("bank_address", text="Bank Address")
        self.documents_tree.heading("pg_vetted_on", text="PG Vetted On")
        self.documents_tree.heading("indemnity_bond_submitted", text="IB Submitted")
        self.documents_tree.heading("indemnity_bond_details", text="Indemnity Bond Details")
        self.documents_tree.heading("ib_vetted_on", text="IB Vetted On")
        
        self.documents_tree.heading("other_docs_details", text="Other Docs Details")
        self.documents_tree.heading("submission_date", text="Submission Date")

        self.documents_tree.column("firm_name", width=100)
        self.documents_tree.column("pg_submitted", width=80)
        self.documents_tree.column("pg_type", width=100)
        self.documents_tree.column("pg_no", width=80)
        self.documents_tree.column("pg_amount", width=80)
        self.documents_tree.column("bank_name", width=100)
        self.documents_tree.column("bank_address", width=120)
        self.documents_tree.column("pg_vetted_on", width=100)
        self.documents_tree.column("indemnity_bond_submitted", width=80)
        self.documents_tree.column("indemnity_bond_details", width=150)
        self.documents_tree.column("ib_vetted_on", width=100)
        
        self.documents_tree.column("other_docs_details", width=150)
        self.documents_tree.column("submission_date", width=100)

        self.documents_tree.bind("<Double-1>", self._on_document_select)
        self.documents_tree.bind("<Button-3>", self._show_context_menu)

        vsb = ttk.Scrollbar(documents_frame, orient="vertical", command=self.documents_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.documents_tree.configure(yscrollcommand=vsb.set)

    def _on_work_id_change(self, *args):
        self.refresh_data()

    def refresh_data(self):
        self._populate_firm_names()
        self.load_firm_documents()

    def _populate_firm_names(self):
        work_id = self.work_id_var.get()
        if work_id:
            all_firms = db_manager.get_unique_firm_names_by_work_id(int(work_id))
            self.firm_name_combobox['values'] = all_firms
            if all_firms:
                self.firm_name_combobox.set(all_firms[0])
            else:
                self.firm_name_combobox.set("")
        else:
            self.firm_name_combobox['values'] = []
            self.firm_name_combobox.set("")

    def _on_firm_name_key_release(self, event):
        search_text = self.firm_name_var.get().lower()
        work_id = self.work_id_var.get()
        if work_id:
            all_firms = db_manager.get_unique_firm_names_by_work_id(int(work_id))
            if search_text == '':
                self.firm_name_combobox['values'] = all_firms
            else:
                filtered_firms = [firm for firm in all_firms if search_text in firm.lower()]
                self.firm_name_combobox['values'] = filtered_firms

    def _on_firm_selected(self, event):
        selected_firm_name = self.firm_name_var.get() # Store the selected firm name
        self._clear_form() # Clear form first
        self.firm_name_combobox.set(selected_firm_name) # Re-set the selected firm name
        work_id = self.work_id_var.get()
        firm_name = self.firm_name_var.get()
        if work_id and firm_name:
            doc = get_firm_document_by_work_and_firm_name(int(work_id), firm_name)
            if doc:
                self.selected_doc_id = doc['id']
                self.pg_submitted_var.set(bool(doc['pg_submitted']))
                self.pg_no_entry.delete(0, tk.END)
                self.pg_no_entry.insert(0, doc['pg_no'] if doc['pg_no'] else "")
                self.pg_amount_entry.delete(0, tk.END)
                self.pg_amount_entry.insert(0, doc['pg_amount'] if doc['pg_amount'] else "")
                self.bank_name_entry.delete(0, tk.END)
                self.bank_name_entry.insert(0, doc['bank_name'] if doc['bank_name'] else "")
                self.bank_address_entry.delete(0, tk.END)
                self.bank_address_entry.insert(0, doc['bank_address'] if doc['bank_address'] else "")
                self.indemnity_bond_submitted_var.set(bool(doc['indemnity_bond_submitted']))
                self.indemnity_bond_details_entry.delete(0, tk.END)
                self.indemnity_bond_details_entry.insert(0, doc['indemnity_bond_details'] if doc['indemnity_bond_details'] else "")
                self.other_docs_details_entry.delete(0, tk.END)
                self.other_docs_details_entry.insert(0, doc['other_docs_details'] if doc['other_docs_details'] else "")
                self.submission_date_var.set(doc['submission_date'] if doc['submission_date'] else "")

                self._toggle_pg_fields()
                self._toggle_indemnity_bond_fields()
                self.add_button.config(state=tk.DISABLED)
                self.update_button.config(state=tk.NORMAL)
            else:
                self._clear_form()
                self.firm_name_combobox.set(selected_firm_name) # Re-set the selected firm name if no doc found
        self.load_firm_documents() # Reload documents to filter by selected firm

    def load_firm_documents(self):
        for item in self.documents_tree.get_children():
            self.documents_tree.delete(item)
        
        work_id = self.work_id_var.get()
        if not work_id:
            return

        documents = get_firm_documents(int(work_id))
        selected_firm = self.firm_name_var.get()
        for doc in documents:
            if not selected_firm or doc[2] == selected_firm: # doc[2] is firm_name
                self.documents_tree.insert("", tk.END, iid=doc[0], values=(
                    doc[2], bool(doc[10]), doc[12], doc[3], doc[4], doc[5], doc[6], doc[13], bool(doc[11]), doc[7], doc[14], doc[8], doc[9]
                ))

    def _add_document(self):
        work_id = self.work_id_var.get()
        if not work_id:
            show_toast(self, "Please select a work first.", "warning")
            return

        firm_name = self.firm_name_var.get()
        pg_no = self.pg_no_entry.get()
        pg_amount_str = self.pg_amount_entry.get()
        bank_name = self.bank_name_entry.get()
        bank_address = self.bank_address_entry.get()
        indemnity_bond_details = self.indemnity_bond_details_entry.get()
        other_docs_details = self.other_docs_details_entry.get()
        submission_date = self.submission_date_var.get()
        pg_type = self.pg_type_var.get()
        pg_vetted_on = self.pg_vetted_on_var.get()
        ib_vetted_on = self.ib_vetted_on_var.get()

        if not all([firm_name, submission_date]):
            show_toast(self, "Firm Name and Submission Date are required.", "warning")
            return

        try:
            pg_amount = float(pg_amount_str) if pg_amount_str else None
            pg_submitted = 1 if self.pg_submitted_var.get() else 0
            indemnity_bond_submitted = 1 if self.indemnity_bond_submitted_var.get() else 0

            add_firm_document(
                int(work_id), firm_name, pg_no, pg_amount, bank_name, bank_address,
                indemnity_bond_details, other_docs_details, submission_date,
                pg_submitted, indemnity_bond_submitted, pg_type, pg_vetted_on, ib_vetted_on
            )
            show_toast(self, "Document added successfully.", "success")
            self._clear_form()
            self.load_firm_documents()
        except Exception as e:
            show_toast(self, f"Error adding document: {e}", "error")

    def _update_document(self):
        if self.selected_doc_id is None:
            show_toast(self, "Please select a document to update.", "warning")
            return

        doc_id = self.selected_doc_id
        firm_name = self.firm_name_var.get()
        pg_no = self.pg_no_entry.get()
        pg_amount_str = self.pg_amount_entry.get()
        bank_name = self.bank_name_entry.get()
        bank_address = self.bank_address_entry.get()
        indemnity_bond_details = self.indemnity_bond_details_entry.get()
        other_docs_details = self.other_docs_details_entry.get()
        submission_date = self.submission_date_var.get()
        pg_type = self.pg_type_var.get()
        pg_vetted_on = self.pg_vetted_on_var.get()
        ib_vetted_on = self.ib_vetted_on_var.get()

        if not all([firm_name, submission_date]):
            show_toast(self, "Firm Name and Submission Date are required.", "warning")
            return

        try:
            pg_amount = float(pg_amount_str) if pg_amount_str else None
            pg_submitted = 1 if self.pg_submitted_var.get() else 0
            indemnity_bond_submitted = 1 if self.indemnity_bond_submitted_var.get() else 0

            update_firm_document(
                doc_id, firm_name, pg_no, pg_amount, bank_name, bank_address,
                indemnity_bond_details, other_docs_details, submission_date,
                pg_submitted, indemnity_bond_submitted, pg_type, pg_vetted_on, ib_vetted_on
            )
            show_toast(self, "Document updated successfully.", "success")
            self._clear_form()
            self.load_firm_documents()
        except Exception as e:
            show_toast(self, f"Error updating document: {e}", "error")

    def _delete_document(self):
        selected_item = self.documents_tree.selection()
        if not selected_item:
            show_toast(self, "Please select a document to delete.", "warning")
            return

        doc_id = int(selected_item[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this document?"):
            try:
                delete_firm_document(doc_id)
                show_toast(self, "Document deleted successfully.", "success")
                self._clear_form()
                self.load_firm_documents()
            except Exception as e:
                show_toast(self, f"Error deleting document: {e}", "error")

    def _on_document_select(self, event):
        selected_item = self.documents_tree.selection()
        if selected_item:
            doc_id = int(selected_item[0])
            values = self.documents_tree.item(selected_item[0], "values")
            
            print(f"Selected doc_id: {doc_id}")
            print(f"Retrieved values from treeview: {values}")

            self.firm_name_combobox.set(values[0])
            self.pg_submitted_var.set(values[1] == 'True')
            self.pg_type_combobox.set(values[2])
            self.pg_no_entry.delete(0, tk.END)
            self.pg_no_entry.insert(0, values[3])
            self.pg_amount_entry.delete(0, tk.END)
            self.pg_amount_entry.insert(0, values[4])
            self.bank_name_entry.delete(0, tk.END)
            self.bank_name_entry.insert(0, values[5])
            self.bank_address_entry.delete(0, tk.END)
            self.bank_address_entry.insert(0, values[6])
            self.pg_vetted_on_var.set(values[7])
            self.indemnity_bond_submitted_var.set(values[8] == 'True')
            self.indemnity_bond_details_entry.delete(0, tk.END)
            self.indemnity_bond_details_entry.insert(0, values[9])
            self.ib_vetted_on_var.set(values[10])
            self.other_docs_details_entry.delete(0, tk.END)
            self.other_docs_details_entry.insert(0, values[11])
            self.submission_date_var.set(values[12])

            self._toggle_pg_fields()
            self._toggle_indemnity_bond_fields()

            self.add_button.config(state=tk.DISABLED)
            self.update_button.config(state=tk.NORMAL)
            self.selected_doc_id = doc_id # Store the ID of the selected document
        else:
            self._clear_form()

    def _clear_form(self):
        self.firm_name_combobox.set("")
        self.pg_submitted_var.set(False)
        self.pg_type_combobox.set("")
        self.pg_no_entry.delete(0, tk.END)
        self.pg_amount_entry.delete(0, tk.END)
        self.bank_name_entry.delete(0, tk.END)
        self.bank_address_entry.delete(0, tk.END)
        self.pg_vetted_on_var.set("")
        self.indemnity_bond_submitted_var.set(False)
        self.indemnity_bond_details_entry.delete(0, tk.END)
        self.ib_vetted_on_var.set("")
        self.other_docs_details_entry.delete(0, tk.END)
        self.submission_date_var.set(datetime.now().strftime("%d-%m-%Y"))
        self.add_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.DISABLED)
        self.documents_tree.selection_remove(self.documents_tree.selection())
        self.selected_doc_id = None # Clear the stored document ID

    def _show_context_menu(self, event):
        item_id = self.documents_tree.identify_row(event.y)
        if item_id:
            self.documents_tree.selection_set(item_id)
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Edit", command=lambda: self._on_document_select(None))
            context_menu.add_command(label="Delete", command=self._delete_document)
            context_menu.post(event.x_root, event.y_root)

    def _toggle_pg_fields(self, event=None):
        state = tk.NORMAL if self.pg_submitted_var.get() else tk.DISABLED
        self.pg_type_combobox.config(state=state)
        self.pg_no_entry.config(state=state)
        self.pg_amount_entry.config(state=state)
        self.bank_name_entry.config(state=state)
        self.bank_address_entry.config(state=state)

        pg_type = self.pg_type_var.get()
        if pg_type in ["FDR – Fixed Deposit Receipt", "SD – Security Deposit", "EMD – Earnest Money Deposit"]:
            self.pg_vetted_on_placeholder = "DD-MM-YYYY"
            self.pg_vetted_on_var.set(self.pg_vetted_on_placeholder if self.pg_submitted_var.get() else "")
        else:
            self.pg_vetted_on_var.set(self.pg_vetted_on_placeholder if state == tk.NORMAL else "")

    def _toggle_indemnity_bond_fields(self):
        state = tk.NORMAL if self.indemnity_bond_submitted_var.get() else tk.DISABLED
        self.indemnity_bond_details_entry.config(state=state)
        # For minimal date picker, we just clear/reset the value based on state
        if state == tk.DISABLED:
            self.ib_vetted_on_var.set("")
        else:
            self.ib_vetted_on_var.set("DD-MM-YYYY")
