import tkinter as tk
from database.db_manager import create_tables
from features.firm_documents.firm_documents_manager import create_firm_documents_table
from features.work_management.main_window import MainWindow
from utils.styles import set_theme

def main():
    create_tables()  # Initialize SQLite database
    create_firm_documents_table() # Create firm documents table
    root = tk.Tk()
    # set_theme() is called by MainWindow now
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()