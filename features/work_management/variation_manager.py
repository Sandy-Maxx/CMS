
import tkinter as tk
from tkinter import ttk, simpledialog
from database import db_manager
from utils import helpers as utils_helpers

class VariationManager:
    def __init__(self, schedule_items_tab, work_id):
        self.schedule_items_tab = schedule_items_tab
        self.work_id = work_id

    def add_variation_column(self):
        schedule_tree = self.schedule_items_tab.get_schedule_tree()
        variation_name = simpledialog.askstring("Input", "Enter Variation Name:", parent=self.schedule_items_tab)
        if not variation_name:
            return

        columns = list(schedule_tree["columns"])
        if variation_name in columns:
            utils_helpers.show_toast(self.schedule_items_tab.parent_app.window, f"Variation '{variation_name}' already exists.", "warning")
            return

        columns.append(variation_name)
        schedule_tree["columns"] = columns
        schedule_tree.heading(variation_name, text=variation_name)
        schedule_tree.column(variation_name, width=90, stretch=tk.NO, anchor=tk.CENTER)

        schedule_items = db_manager.get_schedule_items(self.work_id)
        for item in schedule_items:
            db_manager.add_schedule_item_variation(item['item_id'], variation_name, 0)

        self.schedule_items_tab._load_schedule_items()

    def on_cell_edit(self, event):
        schedule_tree = self.schedule_items_tab.get_schedule_tree()
        region = schedule_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column_id = schedule_tree.identify_column(event.x)
        item_id = schedule_tree.identify_row(event.y)

        if not column_id or not item_id:
            return

        column_name = schedule_tree.heading(column_id)["text"]
        if column_name not in self.get_variation_names():
            schedule_tree.selection_set(item_id)
            self.schedule_items_tab._edit_item()
            return

        column_index = int(column_id.replace("#", "")) - 1
        
        entry_edit = ttk.Entry(schedule_tree, justify='center')
        
        current_values = schedule_tree.item(item_id, "values")
        if column_index >= len(current_values):
            return
        current_value = current_values[column_index]
        
        entry_edit.insert(0, current_value)
        entry_edit.select_range(0, tk.END)
        entry_edit.focus_set()
        
        bbox = schedule_tree.bbox(item_id, column_id)
        entry_edit.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])

        def on_focus_out(event):
            self.save_variation(item_id, column_name, entry_edit.get())
            entry_edit.destroy()

        def on_return_key(event):
            self.save_variation(item_id, column_name, entry_edit.get())
            entry_edit.destroy()

        entry_edit.bind("<FocusOut>", on_focus_out)
        entry_edit.bind("<Return>", on_return_key)

    def save_variation(self, item_id, variation_name, new_quantity):
        try:
            new_quantity = float(new_quantity)
            db_manager.update_schedule_item_variation(item_id, variation_name, new_quantity)
            self.schedule_items_tab._load_schedule_items()
        except (ValueError, TypeError):
            utils_helpers.show_toast(self.schedule_items_tab.parent_app.window, "Invalid quantity.", "error")
        except Exception as e:
            utils_helpers.show_toast(self.schedule_items_tab.parent_app.window, f"Error: {e}", "error")

    def get_variation_names(self):
        return db_manager.get_variation_names_for_work(self.work_id)
