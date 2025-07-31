import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class CompressionDialWidget(ttk.Frame):
    def __init__(self, master, on_compress_callback):
        super().__init__(master, padding=10)
        self.on_compress_callback = on_compress_callback
        self.pdf_path = None
        self.original_file_size = 0 # in bytes

        self.compression_level_var = tk.IntVar(value=5) # Default to middle compression
        self.probable_size_var = tk.StringVar(value="Select PDF to estimate size")

        self._create_widgets()

    def _create_widgets(self):
        # Compression Level Label
        self.level_label = ttk.Label(self, text="Compression Level: 5")
        self.level_label.pack(pady=(0, 5))

        # Scrollable Dial (Scale)
        self.compression_scale = ttk.Scale(
            self,
            from_=0,
            to=10,
            orient="horizontal",
            variable=self.compression_level_var,
            command=self._update_display_values
        )
        self.compression_scale.pack(fill="x", expand=True, pady=(0, 10))

        # Probable Size Label
        self.size_label = ttk.Label(self, textvariable=self.probable_size_var)
        self.size_label.pack(pady=(0, 10))

        # Compress Button (will be handled by parent tab)
        # This widget primarily provides the level and size estimation.
        # The actual compress button will be in the PdfToolTab.

    def set_pdf_path(self, path):
        self.pdf_path = path
        self._calculate_original_size()
        self._update_display_values()

    def _calculate_original_size(self):
        if self.pdf_path and os.path.exists(self.pdf_path):
            self.original_file_size = os.path.getsize(self.pdf_path)
        else:
            self.original_file_size = 0
        self._update_display_values()

    def _update_display_values(self, *args):
        level = self.compression_level_var.get()
        self.level_label.config(text=f"Compression Level: {level}")

        if self.original_file_size > 0:
            # Heuristic for probable size:
            # Level 0: 100% of original size (no compression)
            # Level 10: 20% of original size (80% reduction)
            # Linear interpolation for intermediate levels
            reduction_factor = level / 10.0 * 0.8 # Max 80% reduction
            probable_size_bytes = self.original_file_size * (1 - reduction_factor)
            self.probable_size_var.set(f"Probable Output Size: {self._format_bytes(probable_size_bytes)}")
        else:
            self.probable_size_var.set("Select PDF to estimate size")

    def _format_bytes(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes:.2f} Bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"

    def get_compression_level(self):
        return self.compression_level_var.get()
