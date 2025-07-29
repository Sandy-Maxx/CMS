import tkinter as tk
from tkinter import ttk
from utils.styles import set_theme

class ModernCard(ttk.Frame):
    """A modern card-like frame with padding and styling"""
    def __init__(self, parent, padding=15, **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        self.padding = padding
        
        # Create inner frame for content with padding
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=padding, pady=padding)
    
    def add_content(self, widget):
        """Add content to the card"""
        widget.pack(in_=self.content_frame, fill=tk.BOTH, expand=True)

class ModernButton(ttk.Button):
    """Enhanced button with modern styling and hover effects"""
    def __init__(self, parent, text="", style="Primary.TButton", icon=None, 
                 tooltip=None, **kwargs):
        super().__init__(parent, text=text, style=style, **kwargs)
        
        if icon:
            self.configure(image=icon, compound=tk.LEFT)
        
        # Add hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Add tooltip if provided
        if tooltip:
            self.tooltip = ToolTip(self, tooltip)
    
    def _on_enter(self, event):
        """Handle mouse enter"""
        pass  # Styling is handled by ttk.Style
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        pass  # Styling is handled by ttk.Style

class ModernEntry(ttk.Entry):
    """Enhanced entry with placeholder text and modern styling"""
    def __init__(self, parent, placeholder="", style="Modern.TEntry", **kwargs):
        super().__init__(parent, style=style, **kwargs)
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self._add_placeholder()
    
    def _add_placeholder(self):
        """Add placeholder functionality"""
        self.insert(0, self.placeholder)
        self.placeholder_active = True
        self.configure(foreground='grey')
        
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.configure(foreground='black')
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground='grey')
            self.placeholder_active = True

class ModernCombobox(ttk.Combobox):
    """Enhanced combobox with modern styling"""
    def __init__(self, parent, style="Modern.TCombobox", **kwargs):
        super().__init__(parent, style=style, **kwargs)

class StatusIndicator(ttk.Label):
    """Status indicator with different states"""
    def __init__(self, parent, status="normal", **kwargs):
        self.status_styles = {
            'success': 'Status.Success.TLabel',
            'warning': 'Status.Warning.TLabel', 
            'error': 'Status.Error.TLabel'
        }
        
        style = self.status_styles.get(status, 'TLabel')
        super().__init__(parent, style=style, **kwargs)
    
    def set_status(self, status, text=""):
        """Update status indicator"""
        style = self.status_styles.get(status, 'TLabel')
        self.configure(style=style, text=text)

class ToolTip:
    """Simple tooltip widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        if self.tooltip_window:
            return
        
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip_window, text=self.text,
                        background="#ffffe0", relief="solid", borderwidth=1,
                        font=("Segoe UI", 9))
        label.pack()
    
    def _on_leave(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ModernProgressBar(ttk.Progressbar):
    """Enhanced progress bar with modern styling"""
    def __init__(self, parent, style="Modern.Horizontal.TProgressbar", **kwargs):
        super().__init__(parent, style=style, **kwargs)

class SearchBar(ttk.Frame):
    """Modern search bar component"""
    def __init__(self, parent, on_search=None, placeholder="Search...", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search
        
        # Search icon (you can replace with actual icon)
        self.search_label = ttk.Label(self, text="🔍")
        self.search_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Search entry
        self.search_entry = ModernEntry(self, placeholder=placeholder)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Bind search functionality
        if on_search:
            self.search_entry.bind('<KeyRelease>', self._on_key_release)
            self.search_entry.bind('<Return>', self._on_return)
    
    def _on_key_release(self, event):
        """Handle key release for live search"""
        if self.on_search and not self.search_entry.placeholder_active:
            self.on_search(self.search_entry.get())
    
    def _on_return(self, event):
        """Handle return key press"""
        if self.on_search and not self.search_entry.placeholder_active:
            self.on_search(self.search_entry.get())
    
    def get_search_text(self):
        """Get current search text"""
        if self.search_entry.placeholder_active:
            return ""
        return self.search_entry.get()
    
    def clear(self):
        """Clear search text"""
        self.search_entry.delete(0, tk.END)

class ModernDialog(tk.Toplevel):
    """Modern dialog base class"""
    def __init__(self, parent, title="Dialog", size=(400, 300)):
        super().__init__(parent)
        
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.center_window()
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))
    
    def center_window(self):
        """Center the dialog on the parent window"""
        self.update_idletasks()
        parent = self.master
        
        # Get parent position and size
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - self.winfo_width()) // 2
        y = parent_y + (parent_height - self.winfo_height()) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def add_button(self, text, command, style="TButton"):
        """Add a button to the dialog"""
        button = ModernButton(self.button_frame, text=text, command=command, style=style)
        button.pack(side=tk.RIGHT, padx=(10, 0))
        return button

class SectionHeader(ttk.Frame):
    """Modern section header with title and optional actions"""
    def __init__(self, parent, title, subtitle=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Title
        self.title_label = ttk.Label(self, text=title, style="Header.TLabel")
        self.title_label.pack(anchor=tk.W)
        
        # Subtitle if provided
        if subtitle:
            self.subtitle_label = ttk.Label(self, text=subtitle, style="Status.TLabel")
            self.subtitle_label.pack(anchor=tk.W)
        
        # Separator
        separator = ttk.Separator(self, orient=tk.HORIZONTAL, style="Modern.TSeparator")
        separator.pack(fill=tk.X, pady=(10, 0))

def add_mousewheel_support(widget, canvas=None):
    """Add mouse wheel scrolling support to widgets for Windows, macOS, and Linux"""
    def _on_mousewheel_windows(event):
        """Handle mouse wheel events on Windows and macOS"""
        if canvas:
            # For Canvas widgets
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif hasattr(widget, 'yview_scroll'):
            # For widgets with yview_scroll method (Treeview, Text, Listbox, etc.)
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif hasattr(widget, 'yview'):
            # For widgets with yview method
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_mousewheel_linux_up(event):
        """Handle mouse wheel up events on Linux"""
        if canvas:
            canvas.yview_scroll(-1, "units")
        elif hasattr(widget, 'yview_scroll'):
            widget.yview_scroll(-1, "units")
        elif hasattr(widget, 'yview'):
            widget.yview_scroll(-1, "units")
    
    def _on_mousewheel_linux_down(event):
        """Handle mouse wheel down events on Linux"""
        if canvas:
            canvas.yview_scroll(1, "units")
        elif hasattr(widget, 'yview_scroll'):
            widget.yview_scroll(1, "units")
        elif hasattr(widget, 'yview'):
            widget.yview_scroll(1, "units")
    
    # Bind mouse wheel events for different platforms
    # Windows and macOS
    widget.bind("<MouseWheel>", _on_mousewheel_windows)
    # Linux/Unix
    widget.bind("<Button-4>", _on_mousewheel_linux_up)
    widget.bind("<Button-5>", _on_mousewheel_linux_down)
    
    # For widgets that might have child widgets, bind to them too
    def bind_to_children(parent_widget):
        for child in parent_widget.winfo_children():
            try:
                child.bind("<MouseWheel>", _on_mousewheel_windows)
                child.bind("<Button-4>", _on_mousewheel_linux_up)
                child.bind("<Button-5>", _on_mousewheel_linux_down)
                bind_to_children(child)
            except tk.TclError:
                # Some widgets don't support binding
                pass
    
    bind_to_children(widget)

class ModernTreeview(ttk.Treeview):
    """Enhanced treeview with modern styling and features"""
    def __init__(self, parent, style="Modern.Treeview", **kwargs):
        super().__init__(parent, style=style, **kwargs)
        
        # Add scrollbars
        self.v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        self.h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
        
        self.configure(yscrollcommand=self.v_scrollbar.set, 
                      xscrollcommand=self.h_scrollbar.set)
        
        # Add mouse wheel support
        add_mousewheel_support(self)
    
    def pack_with_scrollbars(self, **pack_kwargs):
        """Pack the treeview with scrollbars"""
        # Create a frame to contain treeview and scrollbars
        container = ttk.Frame(self.master)
        container.pack(**pack_kwargs)
        
        # Pack treeview and scrollbars
        self.pack(in_=container, fill=tk.BOTH, expand=True)
        self.v_scrollbar.pack(in_=container, side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(in_=container, side=tk.BOTTOM, fill=tk.X)
        
        return container

class ActionButton(ttk.Frame):
    """Button with icon and text that can be arranged vertically or horizontally"""
    def __init__(self, parent, text, command, icon=None, orientation="horizontal", **kwargs):
        super().__init__(parent, **kwargs)
        
        if icon:
            self.icon_label = ttk.Label(self, image=icon)
            if orientation == "vertical":
                self.icon_label.pack(pady=(0, 5))
            else:
                self.icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.button = ModernButton(self, text=text, command=command)
        if orientation == "vertical":
            self.button.pack()
        else:
            self.button.pack(side=tk.LEFT)
