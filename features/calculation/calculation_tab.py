import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .calculation_logic import calculate_end_date, calculate_extended_end_date
from utils.date_picker import DatePicker
from dateutil.relativedelta import relativedelta

class CalculationTab(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        # Use a frame for better layout management
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input fields
        ttk.Label(main_frame, text="Starting Date (DD-MM-YYYY):").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.start_date_entry = ttk.Entry(main_frame)
        self.start_date_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        self.start_date_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
        
        # Add a button to open the date picker
        date_picker_button = ttk.Button(main_frame, text="Select Date", command=self._open_start_date_picker)
        date_picker_button.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

        ttk.Label(main_frame, text="Duration:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        duration_frame = ttk.Frame(main_frame)
        duration_frame.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        self.duration_entry = ttk.Entry(duration_frame)
        self.duration_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.duration_unit = ttk.Combobox(duration_frame, values=["Days", "Months", "Years"], state="readonly")
        self.duration_unit.set("Days")
        self.duration_unit.pack(side=tk.RIGHT, padx=(5,0))

        ttk.Label(main_frame, text="Extension Period:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        extension_frame = ttk.Frame(main_frame)
        extension_frame.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        self.extension_period_entry = ttk.Entry(extension_frame)
        self.extension_period_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.extension_unit = ttk.Combobox(extension_frame, values=["Days", "Months", "Years"], state="readonly")
        self.extension_unit.set("Days")
        self.extension_unit.pack(side=tk.RIGHT, padx=(5,0))

        # Calculation button
        calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate_dates)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output labels
        self.end_date_label = ttk.Label(main_frame, text="End Date: ")
        self.end_date_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)

        self.extended_end_date_label = ttk.Label(main_frame, text="Extended End Date: ")
        self.extended_end_date_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)

        # Date Difference Calculation Section
        date_diff_frame = ttk.LabelFrame(main_frame, text="Date Difference Calculation", padding="10")
        date_diff_frame.grid(row=6, column=0, columnspan=3, sticky=tk.EW, pady=10, padx=5)

        ttk.Label(date_diff_frame, text="Start Date (DD-MM-YYYY):").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.diff_start_date_entry = ttk.Entry(date_diff_frame)
        self.diff_start_date_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        self.diff_start_date_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
        diff_start_date_picker_button = ttk.Button(date_diff_frame, text="Select Date", command=self._open_diff_start_date_picker)
        diff_start_date_picker_button.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

        ttk.Label(date_diff_frame, text="End Date (DD-MM-YYYY):").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.diff_end_date_entry = ttk.Entry(date_diff_frame)
        self.diff_end_date_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        self.diff_end_date_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
        diff_end_date_picker_button = ttk.Button(date_diff_frame, text="Select Date", command=self._open_diff_end_date_picker)
        diff_end_date_picker_button.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)

        self.include_dates_var = tk.BooleanVar(value=True)
        include_dates_checkbox = ttk.Checkbutton(date_diff_frame, text="Include Start and End Dates", variable=self.include_dates_var)
        include_dates_checkbox.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5, padx=5)

        calculate_diff_button = ttk.Button(date_diff_frame, text="Calculate Difference", command=self.calculate_date_difference)
        calculate_diff_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.diff_days_label = ttk.Label(date_diff_frame, text="Days: ")
        self.diff_days_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=2, padx=5)
        self.diff_months_label = ttk.Label(date_diff_frame, text="Months: ")
        self.diff_months_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=2, padx=5)
        self.diff_years_label = ttk.Label(date_diff_frame, text="Years: ")
        self.diff_years_label.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=2, padx=5)

        # Configure column weights for resizing
        main_frame.grid_columnconfigure(1, weight=1)
        date_diff_frame.grid_columnconfigure(1, weight=1)

    def _open_start_date_picker(self):
        # Get the absolute position of the entry widget
        x = self.start_date_entry.winfo_rootx()
        y = self.start_date_entry.winfo_rooty() + self.start_date_entry.winfo_height()
        DatePicker(self.controller.root, self.start_date_entry, self.controller, initial_date=self.start_date_entry.get(), x=x, y=y)

    def _open_diff_start_date_picker(self):
        x = self.diff_start_date_entry.winfo_rootx()
        y = self.diff_start_date_entry.winfo_rooty() + self.diff_start_date_entry.winfo_height()
        DatePicker(self.controller.root, self.diff_start_date_entry, self.controller, initial_date=self.diff_start_date_entry.get(), x=x, y=y)

    def _open_diff_end_date_picker(self):
        x = self.diff_end_date_entry.winfo_rootx()
        y = self.diff_end_date_entry.winfo_rooty() + self.diff_end_date_entry.winfo_height()
        DatePicker(self.controller.root, self.diff_end_date_entry, self.controller, initial_date=self.diff_end_date_entry.get(), x=x, y=y)

    def calculate_date_difference(self):
        try:
            start_date_str = self.diff_start_date_entry.get()
            end_date_str = self.diff_end_date_entry.get()
            include_dates = self.include_dates_var.get()

            start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()
            end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()

            if start_date > end_date:
                start_date, end_date = end_date, start_date # Swap to ensure start_date is always earlier

            delta = relativedelta(end_date, start_date)

            days = (end_date - start_date).days
            if include_dates:
                days += 1 # Include both start and end dates

            # Calculate months and years more accurately
            years = delta.years
            months = delta.months
            remaining_days = delta.days

            # Adjust months and years if including dates
            if include_dates:
                if remaining_days == 0 and months == 0 and years == 0:
                    # If dates are the same and included, it's 1 day, 0 months, 0 years
                    days = 1
                elif remaining_days > 0:
                    # If there are remaining days, and we include dates, it means the last month/year is not full
                    # So, we don't increment months/years based on remaining_days for inclusion
                    pass
                elif remaining_days == 0:
                    # If no remaining days, and we include dates, it means the last month/year is full
                    # This is already handled by relativedelta, no further adjustment needed for months/years
                    pass

            self.diff_days_label.config(text=f"Days: {days}")
            self.diff_months_label.config(text=f"Months: {years * 12 + months}") # Total months
            self.diff_years_label.config(text=f"Years: {years}")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure dates are in DD-MM-YYYY format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def calculate_dates(self):
        try:
            start_date_str = self.start_date_entry.get()
            start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()

            duration_value = int(self.duration_entry.get())
            duration_unit = self.duration_unit.get()
            
            end_date = calculate_end_date(start_date, duration_value, duration_unit)
            self.end_date_label.config(text=f"End Date: {end_date.strftime('%d-%m-%Y')}")

            extension_period_text = self.extension_period_entry.get()
            if extension_period_text:
                extension_value = int(extension_period_text)
                extension_unit = self.extension_unit.get()
                extended_end_date = calculate_extended_end_date(end_date, extension_value, extension_unit)
                self.extended_end_date_label.config(text=f"Extended End Date: {extended_end_date.strftime('%d-%m-%Y')}")
            else:
                self.extended_end_date_label.config(text="Extended End Date: ")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure dates are in DD-MM-YYYY format and duration/extension are valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")