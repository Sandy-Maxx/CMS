import tkinter as tk
from database.db_manager import create_tables
from features.work_management.main_window import MainWindow
from utils.styles import configure_styles

def main():
    create_tables()  # Initialize SQLite database
    root = tk.Tk()
    configure_styles() # Configure the ttk styles
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()