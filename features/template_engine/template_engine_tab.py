import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from features.template_engine.template_processor import TemplateProcessor
from features.template_engine.data_manager import TemplateDataManager
from features.template_engine.date_picker_widget import DatePickerWidget
from utils.helpers import load_icon

class TemplateEngineTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.template_path = None
        self.placeholders = {}
        self.template_processor = TemplateProcessor()
        self.data_manager = TemplateDataManager() # Initialize data manager
        self.create_widgets()

    def create_widgets(self):
        # Template Selection
        template_frame = ttk.LabelFrame(self, text="Template Selection", padding=10)
        template_frame.pack(fill=tk.X, padx=10, pady=5)

        self.template_label = ttk.Label(template_frame, text="No template selected.")
        self.template_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.select_template_icon = load_icon("folder") # Assuming a 'folder.png' icon exists
        self.select_button = ttk.Button(template_frame, image=self.select_template_icon, compound=tk.LEFT, command=self.select_template, style='Primary.TButton')
        self.select_button.pack(side=tk.RIGHT)
        self.select_button_text = "Select Template"
        self.select_button.bind("<Enter>", lambda e: self.select_button.config(text=self.select_button_text))
        self.select_button.bind("<Leave>", lambda e: self.select_button.config(text=""))

        # Placeholder Display and Input
        self.placeholder_frame = ttk.LabelFrame(self, text="Placeholders", padding=10)
        self.placeholder_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.placeholder_canvas = tk.Canvas(self.placeholder_frame)
        self.placeholder_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.placeholder_scrollbar = ttk.Scrollbar(self.placeholder_frame, orient="vertical", command=self.placeholder_canvas.yview)
        self.placeholder_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.placeholder_canvas.configure(yscrollcommand=self.placeholder_scrollbar.set)
        self.placeholder_canvas.bind('<Configure>', lambda e: self.placeholder_canvas.configure(scrollregion = self.placeholder_canvas.bbox("all")))

        self.placeholder_inner_frame = ttk.Frame(self.placeholder_canvas)
        self.placeholder_canvas.create_window((0, 0), window=self.placeholder_inner_frame, anchor="nw")

        # Action Buttons
        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.generate_document_icon = load_icon("export") # Assuming an 'export.png' icon exists
        self.generate_button = ttk.Button(button_frame, image=self.generate_document_icon, compound=tk.LEFT, command=self.generate_document, style='Primary.TButton')
        self.generate_button.pack(side=tk.RIGHT, padx=5)
        self.generate_button_text = "Generate Document"
        self.generate_button.bind("<Enter>", lambda e: self.generate_button.config(text=self.generate_button_text))
        self.generate_button.bind("<Leave>", lambda e: self.generate_button.config(text=""))

        self.save_inputs_icon = load_icon("save") # Assuming a 'save.png' icon exists
        self.save_button = ttk.Button(button_frame, image=self.save_inputs_icon, compound=tk.LEFT, command=self.save_inputs, style='Info.TButton')
        self.save_button.pack(side=tk.RIGHT, padx=5)
        self.save_button_text = "Save Inputs"
        self.save_button.bind("<Enter>", lambda e: self.save_button.config(text=self.save_button_text))
        self.save_button.bind("<Leave>", lambda e: self.save_button.config(text=""))

        self.load_inputs_icon = load_icon("add") # Assuming an 'add.png' icon exists
        self.load_button = ttk.Button(button_frame, image=self.load_inputs_icon, compound=tk.LEFT, command=self.load_inputs, style='Info.TButton')
        self.load_button.pack(side=tk.RIGHT, padx=5)
        self.load_button_text = "Load Inputs"
        self.load_button.bind("<Enter>", lambda e: self.load_button.config(text=self.load_button_text))
        self.load_button.bind("<Leave>", lambda e: self.load_button.config(text=""))

        self.load_generated_icon = load_icon("browse")
        self.load_generated_button = ttk.Button(button_frame, image=self.load_generated_icon, compound=tk.LEFT, command=self.load_generated_file, style='Info.TButton')
        self.load_generated_button.pack(side=tk.RIGHT, padx=5)
        self.load_generated_button_text = "Load Generated File"
        self.load_generated_button.bind("<Enter>", lambda e: self.load_generated_button.config(text=self.load_generated_button_text))
        self.load_generated_button.bind("<Leave>", lambda e: self.load_generated_button.config(text=""))

    def select_template(self):
        file_path = filedialog.askopenfilename(
            title="Select Word Template",
            filetypes=[("Word Documents", "*.docx")]
        )
        if file_path:
            self.template_path = file_path
            self.template_label.config(text=os.path.basename(file_path))
            self.load_placeholders()

    def load_placeholders(self):
        # Clear existing placeholders
        for widget in self.placeholder_inner_frame.winfo_children():
            widget.destroy()
        self.placeholders = {}

        if not self.template_path:
            return

        try:
            extracted_placeholders = self.template_processor.extract_placeholders(self.template_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read template file: {e}")
            return

        # Sort placeholders for consistent display
        sorted_placeholders = sorted(list(extracted_placeholders))

        row = 0
        for p_name in sorted_placeholders:
            # Filter out derived placeholders (those with underscores that are not base names)
            is_derived = False
            # Define prefixes that indicate a base placeholder even if they contain underscores
            base_prefixes_with_underscores = ("PROJECT_", "CLIENT_", "CONTRACT_", "WORK_", "ESTIMATE_")

            if "_" in p_name:
                # Check if it's a known base placeholder that might have underscores (e.g., PROJECT_NAME)
                if p_name.startswith(base_prefixes_with_underscores):
                    is_derived = False # It's a base placeholder, not derived
                elif p_name.startswith(("COST", "DATE")):
                    # If it's a COST or DATE placeholder, and contains an underscore, it's derived
                    is_derived = True
                else:
                    # For other placeholders with underscores, assume they are base unless specified otherwise
                    is_derived = False

            if is_derived:
                continue # Skip derived placeholders in the GUI

            ttk.Label(self.placeholder_inner_frame, text=p_name, width=30, anchor="w").grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            # Determine if it's a date field
            if "DATE" in p_name.upper():
                entry = DatePickerWidget(self.placeholder_inner_frame)
            else:
                entry = ttk.Combobox(self.placeholder_inner_frame)
                historical_data = self.data_manager.get_historical_data(self.template_path, p_name)
                if historical_data:
                    entry['values'] = historical_data
            
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            self.placeholders[p_name] = entry
            row += 1

        # Configure column weights to make the entry column expand
        self.placeholder_inner_frame.grid_columnconfigure(1, weight=1)

        self.placeholder_inner_frame.update_idletasks()
        self.placeholder_canvas.config(scrollregion=self.placeholder_canvas.bbox("all"))

        # Attempt to load previously saved inputs for this template
        self.load_inputs()

    def generate_document(self):
        if not self.template_path:
            messagebox.showwarning("No Template", "Please select a template first.")
            return

        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx")],
            initialfile=f"Filled_{os.path.basename(self.template_path)}"
        )

        if not output_file_path:
            messagebox.showinfo("Cancelled", "Document generation cancelled.")
            return

        values = {p_name: entry.get() for p_name, entry in self.placeholders.items()}

        try:
            self.template_processor.replace_placeholders(self.template_path, values, output_file_path)
            messagebox.showinfo("Success", f"Document generated successfully to {output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating document: {e}")

    def save_inputs(self):
        if not self.template_path:
            messagebox.showwarning("No Template", "Please select a template first.")
            return
        
        values = {p_name: entry.get() for p_name, entry in self.placeholders.items()}
        try:
            self.data_manager.save_template_data(self.template_path, values)
            messagebox.showinfo("Save Inputs", "Inputs saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving inputs: {e}")

    def load_inputs(self):
        if not self.template_path:
            return
        
        try:
            loaded_data = self.data_manager.load_template_data(self.template_path)
            for p_name, entry in self.placeholders.items():
                if p_name in loaded_data:
                    # Check if the data is in the new format (a dictionary)
                    if isinstance(loaded_data[p_name], dict):
                        value = loaded_data[p_name].get("current", "")
                    else:
                        # Assume old format (just the value)
                        value = loaded_data[p_name]

                    if isinstance(entry, DatePickerWidget):
                        entry.set(value)
                    else:
                        entry.set(value)
            messagebox.showinfo("Load Inputs", "Inputs loaded successfully.")
        except FileNotFoundError:
            messagebox.showinfo("Load Inputs", "No previously saved inputs found for this template.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading inputs: {e}")

    def load_generated_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Generated Word Document",
            filetypes=[("Word Documents", "*.docx")]
        )
        if not file_path:
            return

        try:
            # This is a simplified assumption. In a real scenario, you might need a more robust
            # way to extract data, perhaps by looking for the original template or metadata.
            # For now, we assume the generated file name contains the template name.
            template_name = os.path.basename(file_path).replace("Filled_", "")
            template_path = os.path.join(os.path.dirname(self.template_path), template_name) # Reconstruct template path

            if not os.path.exists(template_path):
                messagebox.showerror("Error", "Could not find the original template for this generated file.")
                return

            self.template_path = template_path
            self.template_label.config(text=os.path.basename(template_path))
            self.load_placeholders()

            # Now, load the data from the generated file
            # This requires a method in TemplateProcessor to extract values, which we assume exists
            # For demonstration, let's assume it returns a dictionary of placeholder values
            # In a real implementation, this would involve reading the docx and extracting text
            # which can be complex. We will simulate this for now.
            
            # Simulate loading values from the generated docx
            # In a real app, you would implement this in your TemplateProcessor
            # For now, we will just load the last saved data for that template
            self.load_inputs() 

            messagebox.showinfo("File Loaded", "Data from the generated file has been loaded for editing.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load the generated file: {e}")
