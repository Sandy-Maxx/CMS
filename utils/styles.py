from tkinter import ttk

def set_theme(theme_name):
    style = ttk.Style()
    style.theme_use('clam') # Base theme

    if theme_name == "dark":
        # Dark theme colors
        primary_color = "#64FFDA"  # Teal A700
        primary_hover = "#1DE9B6"  # Teal A400
        info_color = "#90CAF9"     # Blue 200
        info_hover = "#64B5F6"     # Blue 300
        warning_color = "#FFD54F"  # Amber 300
        warning_hover = "#FFCA28"  # Amber 400
        danger_color = "#EF9A9A"   # Red 200
        danger_hover = "#E57373"   # Red 300
        secondary_color = "#B0BEC5" # Blue Grey 200
        secondary_hover = "#90A4AE" # Blue Grey 300
        background_color = "#263238" # Blue Grey 900
        text_color = "#ECEFF1"    # Blue Grey 50
        light_text_color = "#90A4AE" # Blue Grey 300
        field_background = "#37474F" # Blue Grey 800
        field_foreground = "#ECEFF1"
        treeview_background = "#37474F"
        treeview_heading_background = "#455A64"

    else: # Default to light theme
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
        field_background = "white"
        field_foreground = text_color
        treeview_background = "white"
        treeview_heading_background = "#B0BEC5"

    # General styles
    style.configure("TFrame", background=background_color)
    style.configure("TLabel", font=("Segoe UI", 10), background=background_color, foreground=text_color)
    style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"), foreground=light_text_color, background=background_color)
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background=treeview_background, fieldbackground=treeview_background, foreground=text_color)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=treeview_heading_background, foreground=text_color)
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

    # Toolbutton style for icon-only buttons
    style.configure("Toolbutton", background=background_color, relief="flat")
    style.map("Toolbutton", background=[('active', '#E0E0E0'), ('pressed', '#B0B0B0')])

    # Entry and Combobox
    style.configure("TEntry", font=("Segoe UI", 10), fieldbackground=field_background, foreground=field_foreground)
    style.configure("TCombobox", font=("Segoe UI", 10), fieldbackground=field_background, foreground=field_foreground)

    # Notebook (Tabs)
    style.configure("TNotebook", background=background_color, borderwidth=0)
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5], background=secondary_color, foreground="white")
    style.map("TNotebook.Tab", background=[('selected', primary_color)], foreground=[('selected', "white")])

    # Toast messages
    style.configure("Toast.TFrame", background=info_color, relief="solid", borderwidth=1, bordercolor=info_hover)
    style.configure("Info.Toast.TLabel", background=info_color, foreground="white", font=("Segoe UI", 9))
    style.configure("Success.Toast.TLabel", background=primary_color, foreground="white", font=("Segoe UI", 9))
    style.configure("Error.Toast.TLabel", background=danger_color, foreground="white", font=("Segoe UI", 9))
    
    # DatePicker styles
    style.configure("DatePicker.Header.TFrame", background=primary_color, relief="raised", borderwidth=1)
    style.configure("DatePicker.Nav.TButton", background=primary_color, foreground="white", font=("Segoe UI", 8, "bold"), relief="flat")
    style.map("DatePicker.Nav.TButton", background=[('active', primary_hover)])
    style.configure("DatePicker.MonthYear.TLabel", background=primary_color, foreground="white", font=("Segoe UI", 9, "bold"))

    style.configure("DatePicker.Days.TFrame", background=background_color, relief="flat", borderwidth=0)
    style.configure("DatePicker.DayHeader.TLabel", background=secondary_color, foreground="white", font=("Segoe UI", 7, "bold"))

    style.configure("DatePicker.Calendar.TFrame", background=field_background, relief="solid", borderwidth=1)
    style.configure("DatePicker.Day.TLabel", background=field_background, foreground=field_foreground, font=("Segoe UI", 7))
    style.configure("DatePicker.Day.TButton", background=field_background, foreground=field_foreground, font=("Segoe UI", 7), relief="flat", borderwidth=1)
    style.map("DatePicker.Day.TButton", background=[('active', secondary_hover), ('selected', info_color)], foreground=[('selected', "white")])

    style.configure("DatePicker.CurrentDay.TButton", background=info_color, foreground="white", font=("Segoe UI", 7, "bold"), relief="solid", borderwidth=1, bordercolor=info_color)
    style.map("DatePicker.CurrentDay.TButton", background=[('active', info_hover)])

    style.configure("DatePicker.Year.TCombobox", fieldbackground=field_background, background=field_background, foreground=field_foreground, font=("Segoe UI", 8))
    style.map("DatePicker.Year.TCombobox", fieldbackground=[('readonly', field_background)])