import tkinter as tk
from tkinter import ttk
from utils.helpers import load_icon

class AboutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Create "About" Tab
        about_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_tab_frame, text="About")

        dev_info_frame = ttk.LabelFrame(about_tab_frame, text="About This Application", padding=15)
        dev_info_frame.pack(pady=20, padx=20, fill=tk.X)

        self.logo_image = load_icon("logo", size=(100, 100))
        if self.logo_image:
            logo_label = ttk.Label(dev_info_frame, image=self.logo_image)
            logo_label.pack(pady=(0, 10))
        else:
            print("Warning: Could not load logo. Make sure 'logo.jpg' exists in assets/icons.")

        ttk.Label(dev_info_frame, text="Designed, Developed, and Written by:", font=('Segoe UI', 10, 'bold')).pack(pady=(0, 5))
        ttk.Label(dev_info_frame, text="Sanjeev Singh Rajput", font=('Segoe UI', 12, 'italic')).pack(pady=(0, 10))
        ttk.Label(dev_info_frame, text="This application is a comprehensive Contract Management System designed for efficiency and ease of use.", wraplength=400, justify=tk.CENTER).pack()

        # Create "Help" Tab
        help_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_tab_frame, text="Help")

        self.accordion_frame = ttk.Frame(help_tab_frame)
        self.accordion_frame.grid_rowconfigure(0, weight=0) # For headers
        self.accordion_frame.grid_columnconfigure(0, weight=1)
        self.accordion_frame.pack(pady=10, padx=0, fill=tk.BOTH, expand=True)

        self.current_accordion_row = 0 # To keep track of the current row for grid

        self.sections = {}

        self._add_faqs_section()
        self._add_template_guide_section()

    def _create_collapsible_section(self, parent, title, content_builder_func):
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.grid(row=self.current_accordion_row, column=0, sticky="ew", pady=2, padx=0)
        self.current_accordion_row += 1
        header_frame.grid(row=self.current_accordion_row, column=0, sticky="ew", pady=2, padx=0)
        self.current_accordion_row += 1

        title_label = ttk.Label(header_frame, text=title, font=('Segoe UI', 10, 'bold'), cursor="hand2")
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5, padx=5)

        arrow_label = ttk.Label(header_frame, text="▼", font=('Segoe UI', 10, 'bold'))
        arrow_label.pack(side=tk.RIGHT, pady=5, padx=5)

        # Create a frame to hold the content, which will be toggled
        content_frame = ttk.Frame(parent)
        # Call the builder function to populate the content_frame
        content_builder_func(content_frame)

        # Place the content_frame in the grid first to get its row information
        content_frame.grid(row=self.current_accordion_row, column=0, sticky="nsew", padx=0, pady=0)
        self.sections[title] = {"content_frame": content_frame, "arrow_label": arrow_label, "is_expanded": False, "row": self.current_accordion_row}
        content_frame.grid_remove() # Hidden by default
        self.current_accordion_row += 1

        title_label.bind("<Button-1>", lambda e: self._toggle_section(title))
        arrow_label.bind("<Button-1>", lambda e: self._toggle_section(title))

    def _add_faqs_section(self):
        def build_faq_content(parent_frame):
            self.faq_canvas = tk.Canvas(parent_frame)
            self.faq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.faq_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.faq_canvas.yview)
            self.faq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.faq_canvas.configure(yscrollcommand=self.faq_scrollbar.set)
            self.faq_canvas.bind('<Configure>', lambda e: self.faq_canvas.configure(scrollregion = self.faq_canvas.bbox("all")))
            self.faq_canvas.bind('<Configure>', lambda e: self.faq_canvas.itemconfig(self.faq_canvas.find_withtag("inner_frame"), width=e.width), add='+')

            self.faq_inner_frame = ttk.Frame(self.faq_canvas)
            self.faq_canvas.create_window((0, 0), window=self.faq_inner_frame, anchor="nw", width=self.faq_canvas.winfo_width(), tags="inner_frame")


            faqs = [
                {
                    "question": "How do I add a new work?",
                    "answer": "Navigate to the 'Works' tab. Click the 'Add New Work' button. Fill in the work details and save. The new work will appear in the list."
                },
                {
                    "question": "How do I add schedule items to a work?",
                    "answer": "Double-click on a work in the 'Works' tab to open its details. Go to the 'Schedule Items' tab. Click 'Add New Item' and fill in the details."
                },
                {
                    "question": "How can I generate reports?",
                    "answer": "In the 'Works' tab, right-click on a work to access the context menu. Select the desired report type (e.g., Variation, Vitiation, Comparison) to generate it."
                },
                {"question": "What is the 'Template Engine'?",
                    "answer": "The 'Template Engine' allows you to select a Word document template (.docx) with placeholders (e.g., {{placeholder}}, [autofill_data]). You can fill these placeholders with user input or data automatically pulled from your selected work, and then generate a new document."
                },
                {
                    "question": "How do I use the 'PDF Tools'?",
                    "answer": "The 'PDF Tools' tab provides functionalities related to PDF documents, such as merging multiple PDFs into one, or extracting specific pages from a PDF."
                },
                {
                    "question": "What are the auto-populated placeholders?",
                    "answer": """The application can automatically populate certain placeholders with data from the selected work. These placeholders are typically enclosed in square brackets `[]` and include:
*   **[ID]**: The unique identifier of the work.
*   **[NAME]**: The name of the work.
*   **[DESCRIPTION]**: A description of the work.
*   **[JUSTIFICATION]**: The justification for the work.
*   **[SECTION]**: The section related to the work.
*   **[WORK_TYPE]**: The type of work.
*   **[FILE_NO]**: The file number associated with the work.
*   **[ESTIMATE_NO]**: The estimate number for the work.
*   **[TENDER_COST]**: The tender cost of the work.
*   **[TENDER_OPENING_DATE]**: The date of tender opening.
*   **[LOA_NO]**: The Letter of Acceptance (LOA) number.
*   **[LOA_DATE]**: The date of the Letter of Acceptance (LOA).
*   **[WORK_COMMENCE_DATE]**: The work commencement date.
*   **[firm_pg_details]**: This special placeholder will be replaced with a formatted block of text containing details of all Performance Guarantees (PGs) submitted by firms for the selected work."""
                },
                {
                    "question": "What are the different types of placeholders?",
                    "answer": """The application uses three types of placeholders in templates:
*   **[PLACEHOLDER]**: These are standard placeholders that you can fill with any text.
*   **<<PLACEHOLDER>>**: These placeholders are designed for numerical values and will be automatically formatted as currency.
*   **{{PLACEHOLDER}}**: These placeholders are for dates and will automatically open a date picker for easy selection."""
                }
            ]

            for i, faq in enumerate(faqs):
                question_frame = ttk.Frame(self.faq_inner_frame, style='Card.TFrame')
                question_frame.pack(fill=tk.X, pady=5, padx=5)

                question_label = ttk.Label(question_frame, text=faq["question"], font=('Segoe UI', 10, 'bold'), cursor="hand2")
                question_label.pack(fill=tk.X, pady=5, padx=5)
                question_label.bind("<Button-1>", lambda e, idx=i: self._toggle_faq_answer(idx))

                answer_label = ttk.Label(question_frame, text=faq["answer"], wraplength=450, justify=tk.LEFT)
                answer_label.pack(fill=tk.X, pady=5, padx=5)
                answer_label.pack_forget() # Hide by default

                self.faq_inner_frame.grid_columnconfigure(0, weight=1)

        self._create_collapsible_section(self.accordion_frame, "Frequently Asked Questions (FAQ)", build_faq_content)

    def _toggle_faq_answer(self, index):
        # Get all answer labels
        answer_labels = [widget for widget in self.faq_inner_frame.winfo_children()[index].winfo_children() if isinstance(widget, ttk.Label) and widget != self.faq_inner_frame.winfo_children()[index].winfo_children()[0]]
        
        if answer_labels:
            answer_label = answer_labels[0]
            if answer_label.winfo_ismapped():
                answer_label.pack_forget()
            else:
                answer_label.pack(fill=tk.X, pady=5, padx=5)

        self.faq_canvas.update_idletasks()
        self.faq_canvas.config(scrollregion=self.faq_canvas.bbox("all"))

    def _add_template_guide_section(self):
        def build_guide_content(parent_frame):
            guide_text_widget = tk.Text(parent_frame, wrap=tk.WORD, height=15, state=tk.DISABLED, font=('Segoe UI', 9))
            guide_text_widget.pack(fill=tk.BOTH, expand=True)

            # Load and display content from the Markdown file as plain text
            import sys
            import os

            try:
                # Determine the base path for the bundled files
                if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                    # Running in a PyInstaller bundle
                    base_path = sys._MEIPASS
                else:
                    # Running in a normal Python environment
                    base_path = os.path.abspath(".")

                guide_file_path = os.path.join(base_path, "prompts", "TEMPLATE_ENGINE.md")
                
                with open(guide_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                guide_text_widget.config(state=tk.NORMAL)
                guide_text_widget.insert(tk.END, content)
                guide_text_widget.config(state=tk.DISABLED)

            except FileNotFoundError:
                guide_text_widget.config(state=tk.NORMAL)
                guide_text_widget.insert(tk.END, "Error: Template guide file not found (prompts/TEMPLATE_ENGINE.md). Please ensure it's bundled correctly.")
                guide_text_widget.config(state=tk.DISABLED)
            except Exception as e:
                guide_text_widget.config(state=tk.NORMAL)
                guide_text_widget.insert(tk.END, f"Error loading template guide: {e}")
                guide_text_widget.config(state=tk.DISABLED)

        self._create_collapsible_section(self.accordion_frame, "Template Engine Placeholders Guide", build_guide_content)

    def _toggle_section(self, title):
        section = self.sections[title]
        if section["is_expanded"]:
            section["content_frame"].grid_remove()
            section["arrow_label"].config(text="▼")
            section["is_expanded"] = False
        else:
            section["content_frame"].grid(row=section["row"], column=0, sticky="nsew", padx=0)
            section["arrow_label"].config(text="▲")
            section["is_expanded"] = True
        # Update scroll region if a canvas is involved (e.g., for FAQ)
        if hasattr(self, 'faq_canvas'):
            self.faq_canvas.update_idletasks()
            self.faq_canvas.config(scrollregion=self.faq_canvas.bbox("all"))

    


    def _toggle_faq_answer(self, index):
        # Get all answer labels
        answer_labels = [widget for widget in self.faq_inner_frame.winfo_children()[index].winfo_children() if isinstance(widget, ttk.Label) and widget != self.faq_inner_frame.winfo_children()[index].winfo_children()[0]]
        
        if answer_labels:
            answer_label = answer_labels[0]
            if answer_label.winfo_ismapped():
                answer_label.pack_forget()
            else:
                answer_label.pack(fill=tk.X, pady=5, padx=5)

        self.faq_canvas.update_idletasks()
        self.faq_canvas.config(scrollregion=self.faq_canvas.bbox("all"))

    

    def _parse_markdown_to_text_widget(self, text_widget, markdown_content):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete('1.0', tk.END)

        lines = markdown_content.split('\n')
        in_code_block = False
        in_table = False
        table_headers = []
        table_column_widths = []

        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if not in_code_block: # End of code block, add a newline for spacing
                    text_widget.insert(tk.END, '\n')
                continue

            if in_code_block:
                text_widget.insert(tk.END, line + '\n', 'code')
                continue

            # Basic Markdown parsing
            if line.startswith('# '):
                text_widget.insert(tk.END, line[2:].strip() + '\n\n', 'h1')
            elif line.startswith('## '):
                text_widget.insert(tk.END, line[3:].strip() + '\n\n', 'h2')
            elif line.startswith('### '):
                text_widget.insert(tk.END, line[4:].strip() + '\n\n', 'h3')
            elif line.strip().startswith('|') and line.strip().endswith('|'):
                # Table parsing
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if '---' in line: # This is the separator line for tables
                    in_table = True
                    # Calculate column widths based on headers
                    if table_headers:
                        table_column_widths = [len(h) for h in table_headers]
                    else: # Fallback if headers not captured yet
                        table_column_widths = [len(p) for p in parts]
                    # Adjust widths for content
                    for i, p in enumerate(parts):
                        if i < len(table_column_widths):
                            table_column_widths[i] = max(table_column_widths[i], len(p))
                    continue # Skip the separator line itself
                
                if in_table:
                    if not table_headers: # First data row after separator is header
                        table_headers = parts
                        formatted_line = " | ".join([p.ljust(table_column_widths[i]) for i, p in enumerate(parts)])
                        text_widget.insert(tk.END, formatted_line + '\n', 'table_header')
                    else:
                        formatted_line = " | ".join([p.ljust(table_column_widths[i]) for i, p in enumerate(parts)])
                        text_widget.insert(tk.END, formatted_line + '\n', 'table_row')
                else: # Not in table, but might be a single line with pipes
                    text_widget.insert(tk.END, line + '\n')
            else:
                # Handle bold text
                processed_line = line
                while '**' in processed_line:
                    start = processed_line.find('**')
                    end = processed_line.find('**', start + 2)
                    if start != -1 and end != -1:
                        text_widget.insert(tk.END, processed_line[:start])
                        text_widget.insert(tk.END, processed_line[start+2:end], 'bold')
                        processed_line = processed_line[end+2:]
                    else:
                        break
                while '__' in processed_line:
                    start = processed_line.find('__')
                    end = processed_line.find('__', start + 2)
                    if start != -1 and end != -1:
                        text_widget.insert(tk.END, processed_line[:start])
                        text_widget.insert(tk.END, processed_line[start+2:end], 'bold')
                        processed_line = processed_line[end+2:]
                    else:
                        break
                text_widget.insert(tk.END, processed_line + '\n')
                in_table = False # Reset table state if line doesn't look like a table row

        text_widget.config(state=tk.DISABLED)
        # Ensure the canvas scroll region is updated after content insertion
        if hasattr(self, 'faq_canvas'):
            self.faq_canvas.update_idletasks()
            self.faq_canvas.config(scrollregion=self.faq_canvas.bbox("all"))
