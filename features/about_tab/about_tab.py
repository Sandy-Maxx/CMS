import tkinter as tk
from tkinter import ttk

class AboutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Developer Information Section
        dev_info_frame = ttk.LabelFrame(self, text="About This Application", padding=15)
        dev_info_frame.pack(pady=20, padx=20, fill=tk.X)

        ttk.Label(dev_info_frame, text="Designed, Developed, and Written by:", font=('Segoe UI', 10, 'bold')).pack(pady=(0, 5))
        ttk.Label(dev_info_frame, text="Sanjeev Singh Rajput", font=('Segoe UI', 12, 'italic')).pack(pady=(0, 10))
        ttk.Label(dev_info_frame, text="This application is a comprehensive Contract Management System designed for efficiency and ease of use.", wraplength=400, justify=tk.CENTER).pack()

        # FAQ Section
        faq_frame = ttk.LabelFrame(self, text="Frequently Asked Questions (FAQ)", padding=15)
        faq_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.faq_canvas = tk.Canvas(faq_frame)
        self.faq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.faq_scrollbar = ttk.Scrollbar(faq_frame, orient="vertical", command=self.faq_canvas.yview)
        self.faq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.faq_canvas.configure(yscrollcommand=self.faq_scrollbar.set)
        self.faq_canvas.bind('<Configure>', lambda e: self.faq_canvas.configure(scrollregion = self.faq_canvas.bbox("all")))

        self.faq_inner_frame = ttk.Frame(self.faq_canvas)
        self.faq_canvas.create_window((0, 0), window=self.faq_inner_frame, anchor="nw")

        self._add_faqs()

    def _add_faqs(self):
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
            {
                "question": "What is the 'Template Engine'?",
                "answer": "The 'Template Engine' allows you to select a Word document template (.docx) with placeholders (e.g., {{placeholder}}, [autofill_data]). You can fill these placeholders with user input or data automatically pulled from your selected work, and then generate a new document."
            },
            {
                "question": "How do I use the 'PDF Tools'?",
                "answer": "The 'PDF Tools' tab provides functionalities related to PDF documents, such as merging multiple PDFs into one, or extracting specific pages from a PDF."
            }
        ]

        for i, faq in enumerate(faqs):
            question_frame = ttk.Frame(self.faq_inner_frame, style='Card.TFrame')
            question_frame.pack(fill=tk.X, pady=5, padx=5)

            question_label = ttk.Label(question_frame, text=faq["question"], font=('Segoe UI', 10, 'bold'), cursor="hand2")
            question_label.pack(fill=tk.X, pady=5, padx=5)
            question_label.bind("<Button-1>", lambda e, idx=i: self._toggle_answer(idx))

            answer_label = ttk.Label(question_frame, text=faq["answer"], wraplength=450, justify=tk.LEFT)
            answer_label.pack(fill=tk.X, pady=5, padx=5)
            answer_label.pack_forget() # Hide by default

            self.faq_inner_frame.grid_columnconfigure(0, weight=1)

    def _toggle_answer(self, index):
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
