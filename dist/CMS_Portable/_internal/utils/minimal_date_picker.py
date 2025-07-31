import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar

class MinimalDatePicker(ttk.Frame):
    def __init__(self, parent, textvariable=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.textvariable = textvariable or tk.StringVar()
        self.current_date = datetime.now()
        
        # Initialize with current date if empty
        if not self.textvariable.get():
            self.textvariable.set(self.current_date.strftime("%d-%m-%Y"))
        
        self._create_widgets()
        self._update_display()
        
        # Calendar popup window
        self.calendar_window = None
        self.view_date = datetime.now()  # Date being viewed in calendar
        
        # Bind variable trace to update display when value changes externally
        self.textvariable.trace_add("write", self._on_variable_change)
    
    def _create_widgets(self):
        # Main clickable date display - make it look like a normal entry
        self.date_button = ttk.Entry(self, width=12, state="readonly", cursor="hand2")
        self.date_button.pack(fill=tk.X)
        self.date_button.bind("<Button-1>", lambda e: self._show_calendar())
        self._update_button_display()

    def _update_button_display(self):
        # Update entry text to show current date
        self.date_button.config(state="normal")
        self.date_button.delete(0, tk.END)
        self.date_button.insert(0, self.textvariable.get())
        self.date_button.config(state="readonly")

    def _show_calendar(self):
        # Hide the current calendar if open
        if self.calendar_window:
            self.calendar_window.destroy()
            self.calendar_window = None
            return  # Toggle behavior: close if already open

        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.wm_overrideredirect(True)  # Remove window decorations
        self.calendar_window.configure(bg="white", relief="solid", bd=1)
        
        # Position calendar next to the date button
        x = self.date_button.winfo_rootx()
        y = self.date_button.winfo_rooty() + self.date_button.winfo_height() + 2
        self.calendar_window.geometry(f"+{x}+{y}")
        
        # Bind Escape key to close calendar
        self.calendar_window.bind("<Escape>", lambda e: self._close_calendar())

        # Create calendar.
        self._create_calendar(self.calendar_window)

    def _create_calendar(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(3, 0), padx=3)

        # Month dropdown
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(header_frame, textvariable=self.month_var, width=7, state="readonly", font=('Arial', 8))
        month_combo['values'] = [f"{calendar.month_name[i][:3]}" for i in range(1, 13)]
        month_combo.pack(side=tk.LEFT, padx=(0, 5))
        month_combo.bind('<<ComboboxSelected>>', self._on_month_selected)

        # Year dropdown
        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(header_frame, textvariable=self.year_var, width=6, state="readonly", font=('Arial', 8))
        current_year = self.view_date.year
        year_combo['values'] = [str(year) for year in range(current_year - 50, current_year + 51)]
        year_combo.pack(side=tk.LEFT)
        year_combo.bind('<<ComboboxSelected>>', self._on_year_selected)

        # Set initial values
        self.month_var.set(calendar.month_name[self.view_date.month][:3])
        self.year_var.set(str(self.view_date.year))

        self.days_frame = ttk.Frame(parent)
        self.days_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=(3, 3))

        # Redraw calendar
        self._draw_calendar()

    def _draw_calendar(self):
        # Clear previous day buttons
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # Day headers
        headers = ["M", "T", "W", "T", "F", "S", "S"]
        for header in headers:
            ttk.Label(self.days_frame, text=header, font=('Arial', 8)).grid(row=0, column=headers.index(header), padx=1)

        # Get month matrix
        month_days = calendar.monthcalendar(self.view_date.year, self.view_date.month)

        # Redraw days
        for i, week in enumerate(month_days):
            for j, day in enumerate(week):
                if day == 0:
                    continue
                day_button = ttk.Button(self.days_frame, text=str(day), width=2,
                                        command=lambda day=day: self._select_day(day))
                day_button.configure(style="Small.TButton")
                day_button.grid(row=i+1, column=j, padx=1, pady=1)

    def _on_month_selected(self, event):
        # Find the month number based on the selected name
        month_name = self.month_var.get()
        for i in range(1, 13):
            if calendar.month_name[i][:3] == month_name:
                selected_month = i
                break
        self.view_date = self.view_date.replace(month=selected_month)
        self._draw_calendar()

    def _on_year_selected(self, event):
        selected_year = int(self.year_var.get())
        self.view_date = self.view_date.replace(year=selected_year)
        self._draw_calendar()

    def _prev_month(self):
        # Navigate to previous month
        first_of_month = self.view_date.replace(day=1)
        prev_month = first_of_month - timedelta(days=1)
        self.view_date = prev_month.replace(day=1)
        self._draw_calendar()

    def _next_month(self):
        # Navigate to next month
        days_in_current_month = calendar.monthrange(self.view_date.year, self.view_date.month)[1]
        next_month = self.view_date.replace(day=days_in_current_month) + timedelta(days=1)
        self.view_date = next_month.replace(day=1)
        self._draw_calendar()

    def _select_day(self, day):
        self.textvariable.set(self.view_date.replace(day=day).strftime("%d-%m-%Y"))
        self._update_button_display()
        self.calendar_window.destroy()
        self.calendar_window = None

    def _close_calendar(self):
        if self.calendar_window:
            self.calendar_window.destroy()
            self.calendar_window = None

    def _update_display(self):
        # Update the button when the text variable changes
        self._update_button_display()
        # Update view date to match selected date
        try:
            date_str = self.textvariable.get()
            if date_str and date_str not in ["DD-MM-YYYY", ""]:
                self.view_date = datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            pass
    
    def _on_variable_change(self, *args):
        self._update_display()
    
    def get(self):
        return self.textvariable.get()
    
    def set(self, value):
        self.textvariable.set(value)

# Test the component
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minimal Calendar Date Picker Test")
    
    date_var = tk.StringVar()
    date_picker = MinimalDatePicker(root, textvariable=date_var)
    date_picker.pack(pady=20)
    
    # Show current value
    result_label = ttk.Label(root, text="Selected date: ")
    result_label.pack(pady=10)
    
    def update_result():
        result_label.config(text=f"Selected date: {date_var.get()}")
        root.after(100, update_result)
    
    update_result()
    root.mainloop()
