
import sqlite3
from tkinter import messagebox
from database.db_manager_oop import DBManager

class FirmManager:
    def __init__(self):
        self.db_manager = DBManager()

    def add_firm(self, firm_data):
        try:
            with self.db_manager as cursor:
                cursor.execute("""
                    INSERT INTO firms (name, representative, address)
                    VALUES (?, ?, ?)
                """, (
                    firm_data['name'],
                    firm_data['representative'],
                    firm_data['address']
                ))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add firm: {e}")
            return False

    def get_all_firms(self):
        try:
            with self.db_manager as cursor:
                cursor.execute("SELECT id, name, representative, address FROM firms")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve firms: {e}")
            return []

    def get_firm_by_id(self, firm_id):
        try:
            with self.db_manager as cursor:
                cursor.execute("SELECT id, name, representative, address FROM firms WHERE id=?", (firm_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve firm: {e}")
            return None

    def update_firm(self, firm_id, firm_data):
        try:
            with self.db_manager as cursor:
                cursor.execute("""
                    UPDATE firms
                    SET name=?, representative=?, address=?
                    WHERE id=?
                """, (
                    firm_data['name'],
                    firm_data['representative'],
                    firm_data['address'],
                    firm_id
                ))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update firm: {e}")
            return False

    def delete_firm(self, firm_id):
        try:
            with self.db_manager as cursor:
                cursor.execute("DELETE FROM firms WHERE id=?", (firm_id,))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete firm: {e}")
            return False
