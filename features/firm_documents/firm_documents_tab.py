import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from features.firm_documents.firm_documents_manager import (
    add_firm_document, get_firm_documents, update_firm_document, delete_firm_document
)
from database import db_manager
from utils.helpers import show_toast, validate_numeric_input
from datetime import datetime

class FirmDocumentsTab(ttk.Frame):
    def __init__(self, parent_notebook, work_id_var):
        super().__init__(parent_notebook)
        self.work_id_var = work_id_var
        self.work_id_var.trace("w", self._on_work_id_change)

        self.vcmd_numeric = self.register(validate_numeric_input)
        self.selected_doc_id = None # To store the ID of the document being edited

        self._create_widgets()
        self.load_firm_documents()

    def _create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self, text="Add/Edit Firm Document")
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

        # PG No.
        ttk.Label(input_frame, text="PG No.:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.pg_no_entry = ttk.Entry(input_frame)
        self.pg_no_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        # PG Amount
        ttk.Label(input_frame, text="PG Amount:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.pg_amount_entry = ttk.Entry(input_frame, validate="key", validatecommand=(self.vcmd_numeric, '%P'))
        self.pg_amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        # Bank Name
        ttk.Label(input_frame, text="Bank Name:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.bank_name_entry = ttk.Entry(input_frame)
        self.bank_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

        # Bank Address
        ttk.Label(input_frame, text="Bank Address:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.bank_address_entry = ttk.Entry(input_frame)
        self.bank_address_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.EW)

        # Indemnity Bond Submitted Checkbox
        self.indemnity_bond_submitted_var = tk.BooleanVar(value=False)
        self.indemnity_bond_submitted_checkbutton = ttk.Checkbutton(input_frame, text="Indemnity Bond Submitted", variable=self.indemnity_bond_submitted_var, command=self._toggle_indemnity_bond_fields)
        self.indemnity_bond_submitted_checkbutton.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        # Indemnity Bond Details
        ttk.Label(input_frame, text="Indemnity Bond Details:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.indemnity_bond_details_entry = ttk.Entry(input_frame)
        self.indemnity_bond_details_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.EW)

        # Firm Address
        ttk.Label(input_frame, text="Firm Address:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.firm_address_entry = ttk.Entry(input_frame)
        self.firm_address_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.EW)

        # Other Docs Details
        ttk.Label(input_frame, text="Other Docs Details:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.other_docs_details_entry = ttk.Entry(input_frame)
        self.other_docs_details_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.EW)

        # Submission Date
        ttk.Label(input_frame, text="Submission Date:").grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.submission_date_entry = ttk.Entry(input_frame)
        self.submission_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.EW)
        self.submission_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d")) # Default to today

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=10)
        self.add_button = ttk.Button(button_frame, text="Add Document", command=self._add_document)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.update_button = ttk.Button(button_frame, text="Update Document", command=self._update_document, state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_form)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        input_frame.grid_columnconfigure(1, weight=1)

        # Documents List
        documents_frame = ttk.LabelFrame(self, text="Firm Documents")
        documents_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.documents_tree = ttk.Treeview(documents_frame, columns=(
            "firm_name", "pg_submitted", "pg_no", "pg_amount", "bank_name", "bank_address",
            "indemnity_bond_submitted", "indemnity_bond_details", "firm_address", "other_docs_details", "submission_date"
        ), show="headings")
        self.documents_tree.pack(fill=tk.BOTH, expand=True)

        self.documents_tree.heading("firm_name", text="Firm Name")
        self.documents_tree.heading("pg_submitted", text="PG Submitted")
        self.documents_tree.heading("pg_no", text="PG No.")
        self.documents_tree.heading("pg_amount", text="PG Amount")
        self.documents_tree.heading("bank_name", text="Bank Name")
        self.documents_tree.heading("bank_address", text="Bank Address")
        self.documents_tree.heading("indemnity_bond_submitted", text="IB Submitted")
        self.documents_tree.heading("indemnity_bond_details", text="Indemnity Bond Details")
        self.documents_tree.heading("firm_address", text="Firm Address")
        self.documents_tree.heading("other_docs_details", text="Other Docs Details")
        self.documents_tree.heading("submission_date", text="Submission Date")

        self.documents_tree.column("firm_name", width=100)
        self.documents_tree.column("pg_submitted", width=80)
        self.documents_tree.column("pg_no", width=80)
        self.documents_tree.column("pg_amount", width=80)
        self.documents_tree.column("bank_name", width=100)
        self.documents_tree.column("bank_address", width=120)
        self.documents_tree.column("indemnity_bond_submitted", width=80)
        self.documents_tree.column("indemnity_bond_details", width=150)
        self.documents_tree.column("firm_address", width=120)
        self.documents_tree.column("other_docs_details", width=150)
        self.documents_tree.column("submission_date", width=100)

        self.documents_tree.bind("<Double-1>", self._on_document_select)
        self.documents_tree.bind("<Button-3>", self._show_context_menu)

        vsb = ttk.Scrollbar(documents_frame, orient="vertical", command=self.documents_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.documents_tree.configure(yscrollcommand=vsb.set)

        # Initial state of fields
        self._toggle_pg_fields()
        self._toggle_indemnity_bond_fields()

    def _on_work_id_change(self, *args):
        self.refresh_data()

    def refresh_data(self):
        self._populate_firm_names()
        self.load_firm_documents()

    def _populate_firm_names(self):
        work_id = self.work_id_var.get()
        if work_id:
            firms_for_work = db_manager.get_unique_firm_names_by_work_id(int(work_id))
            self.firm_name_combobox['values'] = firms_for_work
            if firms_for_work:
                self.firm_name_combobox.set(firms_for_work[0])
            else:
                self.firm_name_combobox.set("")
        else:
            self.firm_name_combobox['values'] = []
            self.firm_name_combobox.set("")

    def _on_firm_name_key_release(self, event):
        search_text = self.firm_name_var.get().lower()
        work_id = self.work_id_var.get()
        if work_id:
            firms_for_work = db_manager.get_unique_firm_names_by_work_id(int(work_id))
            if search_text == '':
                self.firm_name_combobox['values'] = firms_for_work
            else:
                filtered_firms = [firm for firm in firms_for_work if search_text in firm.lower()]
                self.firm_name_combobox['values'] = filtered_firms
        else:
            self.firm_name_combobox['values'] = []

        # This is a bit of a hack to force the dropdown to update
        # when the list of values is changed dynamically.
        self.firm_name_combobox.event_generate('<Down>')
        self.firm_name_combobox.event_generate('<Escape>')

    def _on_firm_selected(self, event):
        self.load_firm_documents() # Reload documents to filter by selected firm
        # Optionally, pre-fill other fields if there's a single document for this firm/work
        # For now, just reloading the list is sufficient to show documents for the selected firm.

    def load_firm_documents(self):
        for item in self.documents_tree.get_children():
            self.documents_tree.delete(item)
        
        work_id = self.work_id_var.get()
        if not work_id:
            return

        documents = get_firm_documents(int(work_id))
        selected_firm = self.firm_name_var.get()
        for doc in documents:
            # doc[0] is id, doc[1] is work_id
            # doc[2] is firm_name, ..., doc[10] is submission_date
            # doc[11] is pg_submitted, doc[12] is indemnity_bond_submitted
            if not selected_firm or doc[2] == selected_firm: # doc[2] is firm_name
                self.documents_tree.insert("", tk.END, iid=doc[0], values=(
                    doc[2], bool(doc[11]), doc[3], doc[4], doc[5], doc[6], bool(doc[12]), doc[7], doc[8], doc[9], doc[10]
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
        firm_address = self.firm_address_entry.get()
        indemnity_bond_details = self.indemnity_bond_details_entry.get()
        other_docs_details = self.other_docs_details_entry.get()
        submission_date = self.submission_date_entry.get()

        if not all([firm_name, submission_date]): # Only firm name and submission date are strictly required
            show_toast(self, "Firm Name and Submission Date are required.", "warning")
            return

        try:
            pg_amount = float(pg_amount_str) if pg_amount_str else None
            pg_submitted = 1 if self.pg_submitted_var.get() else 0
            indemnity_bond_submitted = 1 if self.indemnity_bond_submitted_var.get() else 0

            add_firm_document(
                int(work_id), firm_name, pg_no, pg_amount, bank_name, bank_address,
                firm_address, indemnity_bond_details, other_docs_details, submission_date,
                pg_submitted, indemnity_bond_submitted
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
        firm_address = self.firm_address_entry.get()
        indemnity_bond_details = self.indemnity_bond_details_entry.get()
        other_docs_details = self.other_docs_details_entry.get()
        submission_date = self.submission_date_entry.get()

        if not all([firm_name, submission_date]):
            show_toast(self, "Firm Name and Submission Date are required.", "warning")
            return

        try:
            pg_amount = float(pg_amount_str) if pg_amount_str else None
            pg_submitted = 1 if self.pg_submitted_var.get() else 0
            indemnity_bond_submitted = 1 if self.indemnity_bond_submitted_var.get() else 0

            update_firm_document(
                doc_id, firm_name, pg_no, pg_amount, bank_name, bank_address,
                firm_address, indemnity_bond_details, other_docs_details, submission_date,
                pg_submitted, indemnity_bond_submitted
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
            
            self.firm_name_combobox.set(values[0])
            self.pg_submitted_var.set(values[1])
            self.pg_no_entry.delete(0, tk.END)
            self.pg_no_entry.insert(0, values[2])
            self.pg_amount_entry.delete(0, tk.END)
            self.pg_amount_entry.insert(0, values[3])
            self.bank_name_entry.delete(0, tk.END)
            self.bank_name_entry.insert(0, values[4])
            self.bank_address_entry.delete(0, tk.END)
            self.bank_address_entry.insert(0, values[5])
            self.indemnity_bond_submitted_var.set(values[6])
            self.indemnity_bond_details_entry.delete(0, tk.END)
            self.indemnity_bond_details_entry.insert(0, values[7])
            self.firm_address_entry.delete(0, tk.END)
            self.firm_address_entry.insert(0, values[8])
            self.other_docs_details_entry.delete(0, tk.END)
            self.other_docs_details_entry.insert(0, values[9])
            self.submission_date_entry.delete(0, tk.END)
            self.submission_date_entry.insert(0, values[10])

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
        self.pg_no_entry.delete(0, tk.END)
        self.pg_amount_entry.delete(0, tk.END)
        self.bank_name_entry.delete(0, tk.END)
        self.bank_address_entry.delete(0, tk.END)
        self.indemnity_bond_submitted_var.set(False)
        self.indemnity_bond_details_entry.delete(0, tk.END)
        self.firm_address_entry.delete(0, tk.END)
        self.other_docs_details_entry.delete(0, tk.END)
        self.submission_date_entry.delete(0, tk.END)
        self.submission_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
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

    def _toggle_pg_fields(self):
        state = tk.NORMAL if self.pg_submitted_var.get() else tk.DISABLED
        self.pg_no_entry.config(state=state)
        self.pg_amount_entry.config(state=state)
        self.bank_name_entry.config(state=state)
        self.bank_address_entry.config(state=state)

    def _toggle_indemnity_bond_fields(self):
        state = tk.NORMAL if self.indemnity_bond_submitted_var.get() else tk.DISABLED
        self.indemnity_bond_details_entry.config(state=state)
