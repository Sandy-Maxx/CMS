import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime
from utils.styles import configure_styles

class DatePicker(tk.Toplevel):
    def __init__(self, parent, entry_widget, initial_date=None, x=None, y=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.entry_widget = entry_widget
        self.selected_date = None
        self.current_day = datetime.now().day
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        if initial_date:
            try:
                self.year = datetime.strptime(initial_date, "%d-%m-%Y").year
                self.month = datetime.strptime(initial_date, "%d-%m-%Y").month
            except ValueError:
                self.year = datetime.now().year
                self.month = datetime.now().month
        else:
            self.year = datetime.now().year
            self.month = datetime.now().month

        self.title("Select Date")
        self.resizable(False, False)

        if x is not None and y is not None:
            self.geometry(f"280x280+{x}+{y}") # Increased size to prevent cropping
        else:
            self.geometry("280x280") # Increased size to prevent cropping

        configure_styles() # Apply styles

        self._create_widgets()
        self._show_calendar()

    def _create_widgets(self):
        # Header Frame (Month and Year navigation)
        header_frame = ttk.Frame(self, style="DatePicker.Header.TFrame")
        header_frame.pack(pady=5)

        ttk.Button(header_frame, text="<", command=self._prev_month, style="DatePicker.Nav.TButton").pack(side=tk.LEFT)
        
        # Month selection
        self.month_year_label = ttk.Label(header_frame, text="", width=10, anchor=tk.CENTER, style="DatePicker.MonthYear.TLabel")
        self.month_year_label.pack(side=tk.LEFT, padx=2) # Reduced padx

        # Year selection
        self.year_combobox = ttk.Combobox(header_frame, values=list(range(self.year - 100, self.year + 101)), width=6, state="readonly", style="DatePicker.Year.TCombobox")
        self.year_combobox.set(self.year)
        self.year_combobox.pack(side=tk.LEFT, padx=2) # Reduced padx
        self.year_combobox.bind("<<ComboboxSelected>>", self._on_year_selected)

        ttk.Button(header_frame, text=">", command=self._next_month, style="DatePicker.Nav.TButton").pack(side=tk.LEFT)

        # Day names header
        days_frame = ttk.Frame(self, style="DatePicker.Days.TFrame")
        days_frame.pack()
        for i, day in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            ttk.Label(days_frame, text=day, width=3, anchor=tk.CENTER, style="DatePicker.DayHeader.TLabel").grid(row=0, column=i)

        # Calendar grid
        self.calendar_frame = ttk.Frame(self, style="DatePicker.Calendar.TFrame")
        self.calendar_frame.pack()

    def _on_year_selected(self, event):
        self.year = int(self.year_combobox.get())
        self._show_calendar()

    def _show_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(self.year, self.month)

        self.month_year_label.config(text=f"{calendar.month_name[self.month]}")
        self.year_combobox.set(self.year)

        for week_num, week in enumerate(month_days):
            for day_num, day in enumerate(week):
                if day == 0:
                    ttk.Label(self.calendar_frame, text="", width=3, style="DatePicker.Day.TLabel").grid(row=week_num, column=day_num)
                else:
                    date_str = f"{day:02d}-{self.month:02d}-{self.year}"
                    btn_style = "DatePicker.Day.TButton"
                    if day == self.current_day and self.month == self.current_month and self.year == self.current_year:
                        btn_style = "DatePicker.CurrentDay.TButton"
                    else:
                        btn_style = "DatePicker.Day.TButton" # Ensure all other days use the regular day style
                    btn = ttk.Button(self.calendar_frame, text=str(day), width=3, style=btn_style, command=lambda d=date_str: self._select_date(d))
                    btn.grid(row=week_num, column=day_num)

    def _prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self._show_calendar()

    def _next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self._show_calendar()

    def _select_date(self, date_str):
        self.selected_date = date_str
        self.entry_widget.delete(0, tk.END)
        self.entry_widget.insert(0, date_str)
        self.destroy()

if __name__ == '__main__':
    # Example Usage
    root = tk.Tk()
    root.title("Date Picker Test")

    date_entry = ttk.Entry(root)
    date_entry.pack(pady=20)

    def open_date_picker():
        DatePicker(root, date_entry)

    open_button = ttk.Button(root, text="Open Date Picker", command=open_date_picker)
    open_button.pack()

    root.mainloop()
