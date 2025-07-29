import tkinter as tk
from tkinter import ttk
from utils.helpers import load_icon
from features.template_engine.work_data_provider import WorkDataProvider
from datetime import datetime

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

    def _get_dynamic_placeholder_content(self):
        """Generate dynamic placeholder content that can be refreshed."""
        try:
            placeholders = WorkDataProvider.get_available_placeholders_static()
            
            # Create formatted placeholder text dynamically
            work_placeholders = []
            firm_placeholders = []
            special_placeholders = []
            
            for key, desc in placeholders.items():
                if key.startswith('[') and key.endswith(']'):
                    if key in ('[CURRENT_DATE]', '[CURRENT_TIME]', '[FIRM_PG_DETAILS]', '[ALL_FIRMS_PG_DETAILS]'):
                        special_placeholders.append(f"*   **{key}**: {desc}")
                    else:
                        work_placeholders.append(f"*   **{key}**: {desc}")
                elif key.startswith('<<') and key.endswith('>>'):
                    firm_placeholders.append(f"*   **{key}**: {desc}")
            
            work_placeholders_text = "\n".join(work_placeholders)
            firm_placeholders_text = "\n".join(firm_placeholders) 
            special_placeholders_text = "\n".join(special_placeholders)
            
            # Generate dynamic placeholder list answer
            return f"""Here is the comprehensive list of all available placeholders for the AutoDocGen template system (auto-generated from current database schema):

**WORK DETAILS (use [PLACEHOLDER] format):**
{work_placeholders_text}

**FIRM DETAILS (use <<PLACEHOLDER>> format):**
{firm_placeholders_text}

**SPECIAL PLACEHOLDERS:**
{special_placeholders_text}

**TEMPLATE ENGINE PLACEHOLDERS (use {{{{PLACEHOLDER}}}} format):**
*   **{{{{any_placeholder_name}}}}** - For manual input fields
*   **{{{{COST}}}}** - Base cost value with mathematical operations
*   **{{{{COST_1.1}}}}** - Cost multiplied by 1.1
*   **{{{{COST_IN_WORDS}}}}** - Cost converted to words
*   **{{{{COST_00}}}}** - Cost rounded to nearest 100
*   **{{{{DATE_field}}}}** - Any date field with date picker

**💡 This list is automatically updated when new database fields are added!

(Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"""
            
        except Exception as e:
            return f"Error loading dynamic placeholders: {e}. Please contact support."

    def _add_faqs_section(self):
        def build_faq_content(parent_frame):
            self.faq_canvas = tk.Canvas(parent_frame)
            self.faq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.faq_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.faq_canvas.yview)
            self.faq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.faq_canvas.configure(yscrollcommand=self.faq_scrollbar.set)
            self.faq_canvas.bind('\u003cConfigure\u003e', lambda e: self.faq_canvas.configure(scrollregion = self.faq_canvas.bbox("all")))
            self.faq_canvas.bind('\u003cConfigure\u003e', lambda e: self.faq_canvas.itemconfig(self.faq_canvas.find_withtag("inner_frame"), width=e.width), add='+')

            self.faq_inner_frame = ttk.Frame(self.faq_canvas)
            self.faq_canvas.create_window((0, 0), window=self.faq_inner_frame, anchor="nw", width=self.faq_canvas.winfo_width(), tags="inner_frame")

            # Add mouse wheel scrolling
            def _on_mousewheel(event):
                self.faq_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            self.faq_canvas.bind("<MouseWheel>", _on_mousewheel)
            self.faq_inner_frame.bind("<MouseWheel>", _on_mousewheel)

            # Get dynamic placeholder content using the dedicated method
            dynamic_placeholder_answer = self._get_dynamic_placeholder_content()

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
                    "question": "What are the different types of placeholders?",
                    "answer": """The application uses three types of placeholders in templates:
*   **[PLACEHOLDER]**: These are standard placeholders that you can fill with any text.
*   **<<PLACEHOLDER>>**: These placeholders are designed for numerical values and will be automatically formatted as currency.
*   **{{PLACEHOLDER}}**: These placeholders are for dates and will automatically open a date picker for easy selection."""
                },
                {
                    "question": "Complete List of Available Placeholders for AutoDocGen (Auto-Generated)",
                    "answer": dynamic_placeholder_answer
                },
                {
                    "question": "One-Click Placeholder Copy for AutoDocGen Templates",
                    "answer": "Click the button below to copy all available placeholders to your clipboard, including the newly added ones. You can then paste them into your Word document templates as needed."
                }
            ]

            # Store as instance variable for access in toggle method
            self.faqs = faqs

            for i, faq in enumerate(self.faqs):
                question_frame = ttk.Frame(self.faq_inner_frame, style='Card.TFrame')
                question_frame.pack(fill=tk.X, pady=5, padx=5)

                question_label = ttk.Label(question_frame, text=faq["question"], font=('Segoe UI', 10, 'bold'), cursor="hand2")
                question_label.pack(fill=tk.X, pady=5, padx=5)

                question_label.bind("<Button-1>", lambda e, idx=i: self._toggle_faq_answer(idx))

                # For the two problematic FAQ items, use Text widget with proper state handling
                if "Complete List" in faq["question"] or "One-Click Placeholder Copy" in faq["question"]:
                    # Create text widget with proper state initialization
                    answer_text = tk.Text(question_frame, wrap=tk.WORD, height=20, font=('Segoe UI', 9), 
                                        relief=tk.FLAT, borderwidth=0, selectbackground="#316AC5", 
                                        selectforeground="white", padx=10, pady=5, state=tk.DISABLED)
                    
                    # Enable, insert content, then disable
                    answer_text.config(state=tk.NORMAL)
                    answer_text.insert(tk.END, faq["answer"])
                    answer_text.config(state=tk.DISABLED)
                    
                    # Add vertical scrollbar
                    answer_scrollbar = ttk.Scrollbar(question_frame, orient="vertical", command=answer_text.yview)
                    answer_text.configure(yscrollcommand=answer_scrollbar.set)
                    
                    # Create answer_frame to hold text and scrollbar
                    answer_frame = ttk.Frame(question_frame)
                    
                    # Pack both inside their parent answer_frame
                    answer_text.pack(in_=answer_frame, side=tk.LEFT, fill=tk.BOTH, expand=True)
                    answer_scrollbar.pack(in_=answer_frame, side=tk.RIGHT, fill=tk.Y)
                    
                    answer_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
                    answer_frame.pack_forget()  # Hide by default
                    
                    # Assign answer_frame to faq["answer_widget"] for new toggle logic
                    faq["answer_widget"] = answer_frame
                else:
                    # For regular FAQs, use Label as before
                    answer_label = ttk.Label(question_frame, text=faq["answer"], wraplength=450, justify=tk.LEFT)
                    answer_label.pack(fill=tk.X, pady=5, padx=5)
                    answer_label.pack_forget() # Hide by default
                    
                    # Store direct reference to answer widget
                    faq["answer_widget"] = answer_label

                self.faq_inner_frame.grid_columnconfigure(0, weight=1)

        self._create_collapsible_section(self.accordion_frame, "Frequently Asked Questions (FAQ)", build_faq_content)

    def _toggle_faq_answer(self, idx):
        ans = self.faqs[idx]["answer_widget"]
        if ans.winfo_ismapped():
            ans.pack_forget()
        else:
            ans.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
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
