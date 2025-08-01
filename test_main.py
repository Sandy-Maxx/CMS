import tkinter as tk
import traceback
import sys

def test_gui():
    """Test basic GUI functionality"""
    try:
        print("Testing basic Tkinter...")
        root = tk.Tk()
        root.title("CMS Test - GUI Working!")
        root.geometry("400x200")
        
        label = tk.Label(root, text="CMS Executable Test Successful!\n\nIf you see this window, the executable is working properly.", 
                        font=("Arial", 12), wrapping=300)
        label.pack(pady=50)
        
        button = tk.Button(root, text="Close", command=root.quit, font=("Arial", 10))
        button.pack(pady=10)
        
        print("GUI created successfully, starting mainloop...")
        root.mainloop()
        print("GUI closed normally.")
        
    except Exception as e:
        print(f"Error in GUI: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        input("Press Enter to exit...")

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import tkinter as tk
        print("✓ tkinter")
        
        import sqlite3
        print("✓ sqlite3")
        
        # Test your app imports
        from database.db_manager import create_tables
        print("✓ database.db_manager")
        
        from features.work_management.main_window import MainWindow
        print("✓ MainWindow")
        
        print("All imports successful!")
        return True
        
    except Exception as e:
        print(f"Import error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        input("Press Enter to exit...")
        return False

def main():
    print("=" * 50)
    print("CMS EXECUTABLE TEST")
    print("=" * 50)
    
    # Test imports first
    if not test_imports():
        return
    
    print("\nAll imports successful! Testing GUI...")
    test_gui()

if __name__ == "__main__":
    main()
