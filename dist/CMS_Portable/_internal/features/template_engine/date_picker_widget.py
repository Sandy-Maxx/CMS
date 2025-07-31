import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from utils.helpers import load_icon

class DatePickerWidget(ttk.Frame):
    def __init__(self, parent, initial_date=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.selected_date = initial_date

        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Button-1>", self._show_calendar) # Bind click to show calendar

        self.calendar_icon = load_icon("calendar", size=(16, 16)) # Load a small calendar icon
        self.calendar_button = ttk.Button(self, image=self.calendar_icon, command=self._show_calendar)
        self.calendar_button.pack(side=tk.LEFT)

        if self.selected_date:
            self.entry.insert(0, self.selected_date)

    def _show_calendar(self, event=None):
        top = tk.Toplevel(self.winfo_toplevel())
        top.transient(self.winfo_toplevel()) # Make it transient to the main window
        top.grab_set() # Grab all events until it's destroyed

        # Position the calendar near the button
        self.update_idletasks() # Ensure widget positions are updated
        btn_x = self.calendar_button.winfo_rootx()
        btn_y = self.calendar_button.winfo_rooty()
        top.geometry(f"+{(btn_x)}+{(btn_y)}") # Position at button's top-left

        cal = Calendar(top, selectmode='day',
                       date_pattern='dd-mm-yyyy') # Set Indian date format
        cal.pack(padx=10, pady=10)

        def set_date():
            selected_date_obj = cal.selection_get()
            if selected_date_obj:
                self.selected_date = selected_date_obj.strftime('%d-%m-%Y') # Format to DD-MM-YYYY
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.selected_date)
            top.destroy()

        ttk.Button(top, text="Select", command=set_date).pack(pady=5)

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.selected_date = value
