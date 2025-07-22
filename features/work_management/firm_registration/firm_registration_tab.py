
import tkinter as tk
from tkinter import ttk, messagebox
from features.work_management.firm_registration.firm_manager import FirmManager
from features.work_management.firm_registration.firm_details_dialog import FirmDetailsDialog

class FirmRegistrationTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.firm_manager = FirmManager()

        self.create_widgets()
        self.load_firms()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview to display firms
        self.tree = ttk.Treeview(self.main_frame, columns=("id", "name", "representative", "address"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("representative", text="Representative")
        self.tree.heading("address", text="Address")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Firm", command=self.add_firm)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Firm", command=self.edit_firm)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Firm", command=self.delete_firm)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def load_firms(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        firms = self.firm_manager.get_all_firms()
        for firm in firms:
            self.tree.insert("", tk.END, values=(firm['id'], firm['name'], firm['representative'], firm['address']))

    def add_firm(self):
        dialog = FirmDetailsDialog(self)
        firm_data = dialog.show()

        if firm_data:
            if self.firm_manager.add_firm(firm_data):
                self.load_firms()
                messagebox.showinfo("Success", "Firm added successfully.")
            else:
                messagebox.showerror("Error", "Failed to add firm.")

    def edit_firm(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a firm to edit.")
            return

        item_values = self.tree.item(selected_item, "values")
        firm_id = item_values[0]
        firm_data = {
            'name': item_values[1],
            'representative': item_values[2],
            'address': item_values[3]
        }

        dialog = FirmDetailsDialog(self, firm_data)
        updated_firm_data = dialog.show()

        if updated_firm_data:
            if self.firm_manager.update_firm(firm_id, updated_firm_data):
                self.load_firms()
                messagebox.showinfo("Success", "Firm updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update firm.")

    def delete_firm(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a firm to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected firm?"):
            item_values = self.tree.item(selected_item, "values")
            firm_id = item_values[0]

            if self.firm_manager.delete_firm(firm_id):
                self.load_firms()
                messagebox.showinfo("Success", "Firm deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete firm.")
