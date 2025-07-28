#!/usr/bin/env python3

import tkinter as tk
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from features.work_management.main_window import MainWindow
from database.db_manager import create_tables

def test_ui():
    """Test the UI to ensure Works Management is working"""
    print("Creating database tables...")
    create_tables()
    
    print("Starting UI test...")
    root = tk.Tk()
    root.title("CMS - UI Test")
    root.geometry("1000x700")
    
    try:
        app = MainWindow(root)
        print("✓ MainWindow created successfully")
        print("✓ Works Management tab should be visible")
        print("✓ Action buttons should be displayed")
        print("\nIf you can see the Works Management interface with the works list and action buttons, the fix is working!")
        print("Close the window to end the test.")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creating MainWindow: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()

if __name__ == "__main__":
    test_ui()
