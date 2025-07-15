import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")

_icon_cache = {}

def load_icon(icon_name, size=(36, 36)):
    if icon_name in _icon_cache:
        return _icon_cache[icon_name]
    
    icon_path = os.path.join(ICON_DIR, f"{icon_name}.png")
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file not found: {icon_path}")
        return None
    
    try:
        # Open the image using Pillow
        img = Image.open(icon_path)
        # Resize the image
        img.thumbnail(size, Image.LANCZOS)
        # Convert to ImageTk.PhotoImage
        icon = ImageTk.PhotoImage(img)
        _icon_cache[icon_name] = icon
        return icon
    except Exception as e:
        print(f"Error loading icon {icon_name}: {e}")
        return None

def show_toast(parent, message, toast_type="info"):
    toast = tk.Toplevel(parent)
    toast.overrideredirect(True)
    toast.geometry(f"300x50+{parent.winfo_screenwidth()-350}+50")
    
    if toast_type == "success":
        bg_color = "#d4edda"
        fg_color = "#155724"
    elif toast_type == "error":
        bg_color = "#f8d7da"
        fg_color = "#721c24"
    elif toast_type == "warning":
        bg_color = "#fff3cd"
        fg_color = "#856404"
    else:
        bg_color = "#d1ecf1"
        fg_color = "#0c5460"
    
    frame = ttk.Frame(toast, style="Toast.TFrame")
    frame.pack(fill=tk.BOTH, expand=True)
    ttk.Label(frame, text=message, style=f"{toast_type.capitalize()}.Toast.TLabel", wraplength=280).pack(pady=10, padx=10)
    
    parent.after(3000, toast.destroy)

def validate_numeric_input(new_value):
    if new_value == "":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False

def format_currency_inr(amount):
    # Formats a number as Indian Rupees (INR) with exactly two decimal places
    # Example: 1234567.89 -> ₹ 12,34,567.89
    # Ensure amount is a float and round to 2 decimal places
    amount = float(amount)
    s = f"{amount:.2f}" # Format to exactly two decimal places

    parts = s.split('.')
    integer_part = parts[0]
    decimal_part = parts[1]

    # Format integer part with Indian numbering system
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        other_parts = integer_part[:-3]
        formatted_integer = "" 
        while other_parts:
            formatted_integer = other_parts[-2:] + "," + formatted_integer
            other_parts = other_parts[:-2]
        formatted_integer = formatted_integer + last_three
    else:
        formatted_integer = integer_part

    return f"₹ {formatted_integer}.{decimal_part}/-"

def number_to_indian_words(num):
    from num2words import num2words
    # Handle integers and floats separately
    if isinstance(num, int):
        return num2words(num, lang='en_IN')
    elif isinstance(num, float):
        integer_part = int(num)
        # Round the decimal part to two places before converting to words
        decimal_part = round((num - integer_part) * 100)
        if decimal_part > 0:
            return f"{num2words(integer_part, lang='en_IN')} rupees and {num2words(decimal_part, lang='en_IN')} paise only"
        else:
            return f"{num2words(integer_part, lang='en_IN')} rupees only"
    return str(num)