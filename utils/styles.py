from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Modern theme
    
    # Define a modern color palette
    primary_color = "#4CAF50"  # Green
    primary_hover = "#45a049"
    info_color = "#2196F3"     # Blue
    info_hover = "#1976D2"
    warning_color = "#FFC107"  # Amber
    warning_hover = "#FFA000"
    danger_color = "#F44336"   # Red
    danger_hover = "#D32F2F"
    secondary_color = "#607D8B" # Blue Grey
    secondary_hover = "#455A64"
    background_color = "#ECEFF1" # Light Blue Grey
    text_color = "#263238"    # Dark Blue Grey
    light_text_color = "#78909C" # Medium Blue Grey

    # General styles
    style.configure("TFrame", background=background_color)
    style.configure("TLabel", font=("Segoe UI", 10), background=background_color, foreground=text_color)
    style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"), foreground=light_text_color, background=background_color)
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="white", fieldbackground="white", foreground=text_color)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#CFD8DC", foreground=text_color)
    style.map("Treeview", background=[('selected', primary_color)])
    
    # Buttons
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8, relief="flat", background=secondary_color, foreground="white")
    style.map("TButton", background=[('active', secondary_hover)])

    style.configure("Primary.TButton", background=primary_color, foreground="white")
    style.map("Primary.TButton", background=[('active', primary_hover)])

    style.configure("Info.TButton", background=info_color, foreground="white")
    style.map("Info.TButton", background=[('active', info_hover)])

    style.configure("Warning.TButton", background=warning_color, foreground=text_color) # Warning text usually dark
    style.map("Warning.TButton", background=[('active', warning_hover)])

    style.configure("Danger.TButton", background=danger_color, foreground="white")
    style.map("Danger.TButton", background=[('active', danger_hover)])

    style.configure("Secondary.TButton", background=secondary_color, foreground="white")
    style.map("Secondary.TButton", background=[('active', secondary_hover)])

    # Entry and Combobox
    style.configure("TEntry", font=("Segoe UI", 10), fieldbackground="white", foreground=text_color)
    style.configure("TCombobox", font=("Segoe UI", 10), fieldbackground="white", foreground=text_color)

    # Notebook (Tabs)
    style.configure("TNotebook", background=background_color, borderwidth=0)
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5], background="#B0BEC5", foreground=text_color)
    style.map("TNotebook.Tab", background=[('selected', primary_color)], foreground=[('selected', "white")])

    # Toast messages
    style.configure("Toast.TFrame", background="#E0F2F7", relief="solid", borderwidth=1, bordercolor="#B3E5FC")
    style.configure("Info.Toast.TLabel", background="#E0F2F7", foreground="#01579B", font=("Segoe UI", 9))
    style.configure("Success.Toast.TLabel", background="#E8F5E9", foreground="#1B5E20", font=("Segoe UI", 9))
    style.configure("Error.Toast.TLabel", background="#FFEBEE", foreground="#B71C1C", font=("Segoe UI", 9))
    style.configure("Warning.Toast.TLabel", background="#FFFDE7", foreground="#FF6F00", font=("Segoe UI", 9))