import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from features.pdf_tools.pdf_manager import PdfManager
from features.pdf_tools.compression_dial_widget import CompressionDialWidget
from utils.helpers import load_icon

class PdfToolTab(ttk.Frame):
    def __init__(self, notebook, parent_app):
        super().__init__(notebook, padding=10)
        self.parent_app = parent_app
        self.pdf_manager = PdfManager()

        # Initialize StringVars
        self.merge_output_path_var = tk.StringVar()
        self.extract_input_path_var = tk.StringVar()
        self.pages_to_extract_var = tk.StringVar()
        self.extract_output_path_var = tk.StringVar()
        self.rotate_input_path_var = tk.StringVar()
        self.rotate_page_num_var = tk.StringVar()
        self.rotation_angle_var = tk.StringVar()
        self.delete_input_path_var = tk.StringVar()
        self.delete_page_num_var = tk.StringVar()
        self.compress_input_path_var = tk.StringVar()
        self.compress_output_path_var = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        self.add_files_icon = load_icon("add")
        self.clear_list_icon = load_icon("cancel")
        self.browse_icon = load_icon("browse")
        self.merge_icon = load_icon("merge")
        self.extract_icon = load_icon("extract")
        self.arrange_icon = load_icon("arrange") # New icon for arrange tab

        # Create a notebook for tabs
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Bind events for tab tooltips
        self.tab_control.bind("<Motion>", self._show_tab_tooltip)
        self.tab_control.bind("<Leave>", self._hide_tab_tooltip)
        self.tooltip_window = None # Initialize tooltip window

        # Merge PDFs Tab
        merge_tab = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(merge_tab, text="Merge PDFs") # Use icon for tab
        merge_tab.columnconfigure(0, weight=1)
        merge_tab.columnconfigure(1, weight=1)

        ttk.Label(merge_tab, text="Input PDFs (select multiple):").grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        self.merge_input_paths = []
        self.merge_input_listbox = tk.Listbox(merge_tab, height=5, selectmode=tk.EXTENDED)
        self.merge_input_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Frame for listbox buttons
        listbox_button_frame = ttk.Frame(merge_tab)
        listbox_button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        listbox_button_frame.columnconfigure(0, weight=1)
        listbox_button_frame.columnconfigure(1, weight=1)
        listbox_button_frame.columnconfigure(2, weight=1)
        listbox_button_frame.columnconfigure(3, weight=1)
        
        self.add_files_button = ttk.Button(listbox_button_frame, image=self.add_files_icon, style='Toolbutton', command=self._add_merge_files)
        self.add_files_button.grid(row=0, column=0, sticky="ew", padx=2)
        self.add_files_button.bind("<Enter>", lambda e: self.add_files_button.config(text="Add Files"))
        self.add_files_button.bind("<Leave>", lambda e: self.add_files_button.config(text=""))

        self.clear_list_button = ttk.Button(listbox_button_frame, image=self.clear_list_icon, style='Toolbutton', command=self._clear_merge_list)
        self.clear_list_button.grid(row=0, column=1, sticky="ew", padx=2)
        self.clear_list_button.bind("<Enter>", lambda e: self.clear_list_button.config(text="Clear List"))
        self.clear_list_button.bind("<Leave>", lambda e: self.clear_list_button.config(text=""))

        self.move_up_icon = load_icon("up")
        self.move_down_icon = load_icon("down")

        self.move_up_button = ttk.Button(listbox_button_frame, image=self.move_up_icon, style='Toolbutton', command=self._move_merge_file_up)
        self.move_up_button.grid(row=0, column=2, sticky="ew", padx=2)
        self.move_up_button.bind("<Enter>", lambda e: self.move_up_button.config(text="Move Up"))
        self.move_up_button.bind("<Leave>", lambda e: self.move_up_button.config(text=""))

        self.move_down_button = ttk.Button(listbox_button_frame, image=self.move_down_icon, style='Toolbutton', command=self._move_merge_file_down)
        self.move_down_button.grid(row=0, column=3, sticky="ew", padx=2)
        self.move_down_button.bind("<Enter>", lambda e: self.move_down_button.config(text="Move Down"))
        self.move_down_button.bind("<Leave>", lambda e: self.move_down_button.config(text=""))

        ttk.Label(merge_tab, text="Output Path:").grid(row=3, column=0, sticky="w", pady=5)
        output_path_entry_frame = ttk.Frame(merge_tab)
        output_path_entry_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        output_path_entry_frame.columnconfigure(0, weight=1) # Entry takes most space

        ttk.Entry(output_path_entry_frame, textvariable=self.merge_output_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_merge_output_button = ttk.Button(output_path_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_output_path(self.merge_output_path_var, "merged.pdf"))
        self.browse_merge_output_button.grid(row=0, column=1, sticky="e")
        self.browse_merge_output_button.bind("<Enter>", lambda e: self.browse_merge_output_button.config(text="Browse"))
        self.browse_merge_output_button.bind("<Leave>", lambda e: self.browse_merge_output_button.config(text=""))

        self.merge_pdfs_button = ttk.Button(merge_tab, text="Merge PDFs", image=self.merge_icon, compound=tk.LEFT, command=self._merge_pdfs, style='Primary.TButton')
        self.merge_pdfs_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.merge_pdfs_button.bind("<Enter>", lambda e: self.merge_pdfs_button.config(text="Merge PDFs"))
        self.merge_pdfs_button.bind("<Leave>", lambda e: self.merge_pdfs_button.config(text=""))

        # Extract Pages Tab
        extract_tab = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(extract_tab, text="Extract Pages")
        extract_tab.columnconfigure(0, weight=1)
        extract_tab.columnconfigure(1, weight=1)

        ttk.Label(extract_tab, text="Input PDF:").grid(row=0, column=0, sticky="w", pady=5)
        extract_input_entry_frame = ttk.Frame(extract_tab)
        extract_input_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        extract_input_entry_frame.columnconfigure(0, weight=1)

        ttk.Entry(extract_input_entry_frame, textvariable=self.extract_input_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_extract_input_button = ttk.Button(extract_input_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_input_path(self.extract_input_path_var))
        self.browse_extract_input_button.grid(row=0, column=1, sticky="e")
        self.browse_extract_input_button.bind("<Enter>", lambda e: self.browse_extract_input_button.config(text="Browse"))
        self.browse_extract_input_button.bind("<Leave>", lambda e: self.browse_extract_input_button.config(text=""))

        ttk.Label(extract_tab, text="Pages to Extract (e.g., 1,3-5,7):").grid(row=2, column=0, sticky="w", pady=5)
        self.pages_to_extract_var = tk.StringVar()
        ttk.Entry(extract_tab, textvariable=self.pages_to_extract_var).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(extract_tab, text="Output Path:").grid(row=3, column=0, sticky="w", pady=5)
        extract_output_entry_frame = ttk.Frame(extract_tab)
        extract_output_entry_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        extract_output_entry_frame.columnconfigure(0, weight=1)

        ttk.Entry(extract_output_entry_frame, textvariable=self.extract_output_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_extract_output_button = ttk.Button(extract_output_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_output_path(self.extract_output_path_var, "extracted.pdf"))
        self.browse_extract_output_button.grid(row=0, column=1, sticky="e")
        self.browse_extract_output_button.bind("<Enter>", lambda e: self.browse_extract_output_button.config(text="Browse"))
        self.browse_extract_output_button.bind("<Leave>", lambda e: self.browse_extract_output_button.config(text=""))

        self.extract_pages_button = ttk.Button(extract_tab, text="Extract Pages", image=self.extract_icon, compound=tk.LEFT, command=self._extract_pages, style='Info.TButton')
        self.extract_pages_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.extract_pages_button.bind("<Enter>", lambda e: self.extract_pages_button.config(text="Extract Pages"))
        self.extract_pages_button.bind("<Leave>", lambda e: self.extract_pages_button.config(text=""))

        # Arrange Pages Tab
        arrange_tab = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(arrange_tab, text="Arrange Pages")
        arrange_tab.columnconfigure(0, weight=1)
        arrange_tab.columnconfigure(1, weight=1)

        # Compress PDF Tab
        compress_tab = ttk.Frame(self.tab_control, padding=10)
        self.tab_control.add(compress_tab, text="Compress PDF")
        compress_tab.columnconfigure(0, weight=1)
        compress_tab.columnconfigure(1, weight=1)

        ttk.Label(compress_tab, text="Input PDF:").grid(row=0, column=0, sticky="w", pady=5)
        compress_input_entry_frame = ttk.Frame(compress_tab)
        compress_input_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        compress_input_entry_frame.columnconfigure(0, weight=1)

        self.compress_input_path_var = tk.StringVar()
        ttk.Entry(compress_input_entry_frame, textvariable=self.compress_input_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_compress_input_button = ttk.Button(compress_input_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_input_path(self.compress_input_path_var))
        self.browse_compress_input_button.grid(row=0, column=1, sticky="e")
        self.browse_compress_input_button.bind("<Enter>", lambda e: self.browse_compress_input_button.config(text="Browse"))
        self.browse_compress_input_button.bind("<Leave>", lambda e: self.browse_compress_input_button.config(text=""))

        ttk.Label(compress_tab, text="Output Path:").grid(row=1, column=0, sticky="w", pady=5)
        compress_output_entry_frame = ttk.Frame(compress_tab)
        compress_output_entry_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        compress_output_entry_frame.columnconfigure(0, weight=1)

        self.compress_output_path_var = tk.StringVar()
        ttk.Entry(compress_output_entry_frame, textvariable=self.compress_output_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_compress_output_button = ttk.Button(compress_output_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_output_path(self.compress_output_path_var, "compressed.pdf"))
        self.browse_compress_output_button.grid(row=0, column=1, sticky="e")
        self.browse_compress_output_button.bind("<Enter>", lambda e: self.browse_compress_output_button.config(text="Browse"))
        self.browse_compress_output_button.bind("<Leave>", lambda e: self.browse_compress_output_button.config(text=""))

        self.compress_dial_widget = CompressionDialWidget(compress_tab, self._compress_pdf)
        self.compress_dial_widget.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.compress_pdf_button = ttk.Button(compress_tab, text="Compress PDF", image=self.extract_icon, compound=tk.LEFT, command=self._compress_pdf, style='Info.TButton')
        self.compress_pdf_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.compress_pdf_button.bind("<Enter>", lambda e: self.compress_pdf_button.config(text="Compress PDF"))
        self.compress_pdf_button.bind("<Leave>", lambda e: self.compress_pdf_button.config(text=""))

        # Rotate Page Section
        rotate_frame = ttk.LabelFrame(arrange_tab, text="Rotate Page", padding=10)
        rotate_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        rotate_frame.columnconfigure(0, weight=1)
        rotate_frame.columnconfigure(1, weight=1)

        ttk.Label(rotate_frame, text="Input PDF:").grid(row=0, column=0, sticky="w", pady=5)
        rotate_input_entry_frame = ttk.Frame(rotate_frame)
        rotate_input_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        rotate_input_entry_frame.columnconfigure(0, weight=1)
        ttk.Entry(rotate_input_entry_frame, textvariable=self.rotate_input_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_rotate_input_button = ttk.Button(rotate_input_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_input_path(self.rotate_input_path_var))
        self.browse_rotate_input_button.grid(row=0, column=1, sticky="e")
        self.browse_rotate_input_button.bind("<Enter>", lambda e: self.browse_rotate_input_button.config(text="Browse"))
        self.browse_rotate_input_button.bind("<Leave>", lambda e: self.browse_rotate_input_button.config(text=""))

        ttk.Label(rotate_frame, text="Page Number (1-indexed):").grid(row=1, column=0, sticky="w", pady=5)
        self.rotate_page_num_var = tk.StringVar()
        rotate_page_num_entry = ttk.Entry(rotate_frame, textvariable=self.rotate_page_num_var)
        rotate_page_num_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        rotate_page_num_entry.insert(0, "e.g., 1") # Placeholder
        rotate_page_num_entry.bind("<FocusIn>", lambda e: rotate_page_num_entry.delete(0, tk.END) if rotate_page_num_entry.get() == "e.g., 1" else None)
        rotate_page_num_entry.bind("<FocusOut>", lambda e: rotate_page_num_entry.insert(0, "e.g., 1") if not rotate_page_num_entry.get() else None)

        ttk.Label(rotate_frame, text="Rotation Angle:").grid(row=2, column=0, sticky="w", pady=5)
        self.rotation_angle_var = tk.StringVar()
        rotation_angle_combobox = ttk.Combobox(rotate_frame, textvariable=self.rotation_angle_var, values=[90, 180, 270], state="readonly")
        rotation_angle_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        rotation_angle_combobox.set(90) # Default value

        self.rotate_page_button = ttk.Button(rotate_frame, text="Rotate Page", image=self.extract_icon, compound=tk.LEFT, command=self._rotate_page, style='Info.TButton')
        self.rotate_page_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.rotate_page_button.bind("<Enter>", lambda e: self.rotate_page_button.config(text="Rotate Page"))
        self.rotate_page_button.bind("<Leave>", lambda e: self.rotate_page_button.config(text=""))

        # Delete Page Section
        delete_frame = ttk.LabelFrame(arrange_tab, text="Delete Page", padding=10)
        delete_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        delete_frame.columnconfigure(0, weight=1)
        delete_frame.columnconfigure(1, weight=1)

        ttk.Label(delete_frame, text="Input PDF:").grid(row=0, column=0, sticky="w", pady=5)
        delete_input_entry_frame = ttk.Frame(delete_frame)
        delete_input_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        delete_input_entry_frame.columnconfigure(0, weight=1)
        ttk.Entry(delete_input_entry_frame, textvariable=self.delete_input_path_var).grid(row=0, column=0, sticky="ew")
        self.browse_delete_input_button = ttk.Button(delete_input_entry_frame, image=self.browse_icon, style='Toolbutton', command=lambda: self._browse_input_path(self.delete_input_path_var))
        self.browse_delete_input_button.grid(row=0, column=1, sticky="e")
        self.browse_delete_input_button.bind("<Enter>", lambda e: self.browse_delete_input_button.config(text="Browse"))
        self.browse_delete_input_button.bind("<Leave>", lambda e: self.browse_delete_input_button.config(text=""))

        ttk.Label(delete_frame, text="Page Number (1-indexed):").grid(row=1, column=0, sticky="w", pady=5)
        self.delete_page_num_var = tk.StringVar()
        delete_page_num_entry = ttk.Entry(delete_frame, textvariable=self.delete_page_num_var)
        delete_page_num_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        delete_page_num_entry.insert(0, "e.g., 1") # Placeholder
        delete_page_num_entry.bind("<FocusIn>", lambda e: delete_page_num_entry.delete(0, tk.END) if delete_page_num_entry.get() == "e.g., 1" else None)
        delete_page_num_entry.bind("<FocusOut>", lambda e: delete_page_num_entry.insert(0, "e.g., 1") if not delete_page_num_entry.get() else None)

        self.delete_page_button = ttk.Button(delete_frame, text="Delete Page", image=self.clear_list_icon, compound=tk.LEFT, command=self._delete_page, style='Danger.TButton')
        self.delete_page_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.delete_page_button.bind("<Enter>", lambda e: self.delete_page_button.config(text="Delete Page"))
        self.delete_page_button.bind("<Leave>", lambda e: self.delete_page_button.config(text=""))

    def _show_tab_tooltip(self, event):
        tab_texts = {
            0: "Merge PDFs",
            1: "Extract Pages",
            2: "Arrange Pages",
            3: "Compress PDF",
        }
        try:
            index = self.tab_control.index(f"@{event.x},{event.y}")
            tab_text = tab_texts.get(index)
            if tab_text:
                if not hasattr(self, "tooltip_win") or self.tooltip_win is None:
                    self.tooltip_win = tk.Toplevel(self)
                    self.tooltip_win.wm_overrideredirect(True)
                    self.tooltip_label = ttk.Label(self.tooltip_win, text="", background="#FFFFEA", relief="solid", borderwidth=1)
                    self.tooltip_label.pack()
                self.tooltip_label.config(text=tab_text)
                self.tooltip_win.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
                self.tooltip_win.deiconify()
            else:
                self._hide_tab_tooltip()
        except tk.TclError:
            self._hide_tab_tooltip()

    def _hide_tab_tooltip(self, event=None):
        if hasattr(self, "tooltip_win") and self.tooltip_win:
            self.tooltip_win.withdraw()

    def _add_tooltip(self, widget, text):
        tool_tip = ToolTip(widget, text)
        widget.bind("<Enter>", tool_tip.show)
        widget.bind("<Leave>", tool_tip.hide)

    def _add_merge_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if files:
            for f in files:
                self.merge_input_listbox.insert(tk.END, f)
                self.merge_input_paths.append(f)

    def _clear_merge_list(self):
        self.merge_input_listbox.delete(0, tk.END)
        self.merge_input_paths = []

    def _move_merge_file_up(self):
        selected_indices = self.merge_input_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a PDF to move.")
            return

        for i in selected_indices:
            if i > 0:
                # Move in listbox
                text = self.merge_input_listbox.get(i)
                self.merge_input_listbox.delete(i)
                self.merge_input_listbox.insert(i - 1, text)
                # Move in internal list
                self.merge_input_paths[i], self.merge_input_paths[i-1] = self.merge_input_paths[i-1], self.merge_input_paths[i]
                # Update selection
                self.merge_input_listbox.selection_set(i - 1)

    def _move_merge_file_down(self):
        selected_indices = self.merge_input_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a PDF to move.")
            return

        # Iterate in reverse to avoid issues with changing indices
        for i in reversed(selected_indices):
            if i < self.merge_input_listbox.size() - 1:
                # Move in listbox
                text = self.merge_input_listbox.get(i)
                self.merge_input_listbox.delete(i)
                self.merge_input_listbox.insert(i + 1, text)
                # Move in internal list
                self.merge_input_paths[i], self.merge_input_paths[i+1] = self.merge_input_paths[i+1], self.merge_input_paths[i]
                # Update selection
                self.merge_input_listbox.selection_set(i + 1)

    def _browse_output_path(self, path_var, default_filename):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=default_filename)
        if file_path:
            path_var.set(file_path)

    def _browse_input_path(self, path_var):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            path_var.set(file_path)
            if path_var == self.compress_input_path_var:
                self.compress_dial_widget.set_pdf_path(file_path)

    def _merge_pdfs(self):
        if not self.merge_input_paths:
            messagebox.showwarning("Input Error", "Please add PDF files to merge.")
            return
        output_path = self.merge_output_path_var.get()
        if not output_path:
            messagebox.showwarning("Input Error", "Please specify an output path.")
            return
        
        if self.pdf_manager.merge_pdfs(self.merge_input_paths, output_path):
            messagebox.showinfo("Success", "PDFs merged successfully!")
            self._clear_merge_list()
            self.merge_output_path_var.set("")
        else:
            messagebox.showerror("Error", "Failed to merge PDFs. Check console for details.")

    def _extract_pages(self):
        input_path = self.extract_input_path_var.get()
        if not input_path:
            messagebox.showwarning("Input Error", "Please select an input PDF.")
            return
        output_path = self.extract_output_path_var.get()
        if not output_path:
            messagebox.showwarning("Input Error", "Please specify an output path.")
            return
        pages_str = self.pages_to_extract_var.get()
        if not pages_str:
            messagebox.showwarning("Input Error", "Please specify pages to extract.")
            return

        pages_to_extract_indices = []
        try:
            # Parse page ranges (e.g., "1,3-5,7")
            for part in pages_str.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    pages_to_extract_indices.extend(range(start - 1, end)) # 0-indexed
                else:
                    pages_to_extract_indices.append(int(part) - 1) # 0-indexed
        except ValueError:
            messagebox.showerror("Input Error", "Invalid page format. Use e.g., 1,3-5,7")
            return
        
        if self.pdf_manager.extract_pages(input_path, output_path, pages_to_extract_indices):
            messagebox.showinfo("Success", "Pages extracted successfully!")
            self.extract_input_path_var.set("")
            self.pages_to_extract_var.set("")
            self.extract_output_path_var.set("")
        else:
            messagebox.showerror("Error", "Failed to extract pages. Check console for details.")

    def _rotate_page(self):
        input_path = self.rotate_input_path_var.get()
        if not input_path:
            messagebox.showwarning("Input Error", "Please select an input PDF.")
            return
        page_num_str = self.rotate_page_num_var.get()
        if not page_num_str:
            messagebox.showwarning("Input Error", "Please specify the page number to rotate.")
            return
        rotation_angle_str = self.rotation_angle_var.get()
        if not rotation_angle_str:
            messagebox.showwarning("Input Error", "Please specify the rotation angle.")
            return

        try:
            page_number = int(page_num_str) - 1 # Convert to 0-indexed
            rotation_angle = int(rotation_angle_str)
            if rotation_angle not in [90, 180, 270]:
                messagebox.showerror("Input Error", "Rotation angle must be 90, 180, or 270.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Invalid page number or rotation angle.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"rotated_page_{page_number + 1}.pdf"
        )
        if not output_path:
            messagebox.showinfo("Info", "Operation cancelled.")
            return

        if self.pdf_manager.rotate_page(input_path, output_path, page_number, rotation_angle):
            messagebox.showinfo("Success", f"Page {page_number + 1} rotated successfully and saved to {output_path}")
            self.rotate_input_path_var.set("")
            self.rotate_page_num_var.set("")
            self.rotation_angle_var.set("")
        else:
            messagebox.showerror("Error", "Failed to rotate page. Check console for details.")

    def _delete_page(self):
        input_path = self.delete_input_path_var.get()
        if not input_path:
            messagebox.showwarning("Input Error", "Please select an input PDF.")
            return
        page_num_str = self.delete_page_num_var.get()
        if not page_num_str:
            messagebox.showwarning("Input Error", "Please specify the page number to delete.")
            return

        try:
            page_number = int(page_num_str) - 1 # Convert to 0-indexed
        except ValueError:
            messagebox.showerror("Input Error", "Invalid page number.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"deleted_page_{page_number + 1}.pdf"
        )
        if not output_path:
            messagebox.showinfo("Info", "Operation cancelled.")
            return

        if self.pdf_manager.delete_page(input_path, output_path, page_number):
            messagebox.showinfo("Success", f"Page {page_number + 1} deleted successfully and saved to {output_path}")
            self.delete_input_path_var.set("")
            self.delete_page_num_var.set("")
        else:
            messagebox.showerror("Error", "Failed to delete page. Check console for details.")

    def _compress_pdf(self):
        input_path = self.compress_input_path_var.get()
        if not input_path:
            messagebox.showwarning("Input Error", "Please select an input PDF.")
            return
        output_path = self.compress_output_path_var.get()
        if not output_path:
            messagebox.showwarning("Input Error", "Please specify an output path.")
            return

        if input_path == output_path:
            messagebox.showwarning("Input Error", "Output file cannot be the same as the input file. Please choose a different output path.")
            return

        compression_level = self.compress_dial_widget.get_compression_level()
        if self.pdf_manager.compress_pdf(input_path, output_path, compression_level):
            messagebox.showinfo("Success", "PDF compressed successfully!")
            self.compress_input_path_var.set("")
            self.compress_output_path_var.set("")
        else:
            messagebox.showerror("Error", "Failed to compress PDF. Check console for details.")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.x = 0
        self.y = 0

    def show(self, event=None):
        if self.tooltip_window or not self.text:
            return
        self.x, self.y, cx, cy = self.widget.bbox("insert")
        self.x += self.widget.winfo_rootx() + 25
        self.y += self.widget.winfo_rooty() + 20

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{self.x}+{self.y}")

        label = ttk.Label(self.tooltip_window, text=self.text, background="#FFFFEA", relief="solid", borderwidth=1,
                          font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

        # Arrange Pages (Placeholder for future expansion within this tab)
        arrange_tab.rowconfigure(1, weight=1) # Give space for future arrangement widgets
        arrange_tab.columnconfigure(0, weight=1)
        arrange_tab.columnconfigure(1, weight=1)
