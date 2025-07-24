
import pandas as pd
from database import db_manager

class ScheduleItemBulkManager:
    def __init__(self):
        pass

    def import_schedule_items_from_excel(self, file_path, work_id):
        try:
            df = pd.read_excel(file_path)
            imported_count = 0
            for index, row in df.iterrows():
                item_name = row.get('Item Name')
                quantity = row.get('Quantity')
                unit = row.get('Unit')
                parent_item_id = row.get('Parent Item ID')

                if item_name and quantity is not None and unit:
                    # Ensure parent_item_id is None if not provided or invalid
                    if pd.isna(parent_item_id):
                        parent_item_id = None

                    item_id = db_manager.add_schedule_item(
                        work_id, item_name, unit, quantity, parent_item_id
                    )
                    if item_id:
                        imported_count += 1
            return True, f"Successfully imported {imported_count} schedule items."
        except Exception as e:
            return False, f"Error importing data: {e}"

    def export_schedule_items_to_excel(self, file_path, work_id):
        try:
            schedule_items = db_manager.get_schedule_items(work_id)
            df = pd.DataFrame(schedule_items, columns=[
                'item_id', 'parent_item_id', 'item_name', 'quantity', 'unit'
            ])
            # Rename columns for clarity in the exported file
            df = df.rename(columns={
                'item_id': 'Item ID',
                'parent_item_id': 'Parent Item ID',
                'item_name': 'Item Name',
                'quantity': 'Quantity',
                'unit': 'Unit'
            })
            df.to_excel(file_path, index=False)
            return True, f"Successfully exported {len(schedule_items)} schedule items."
        except Exception as e:
            return False, f"Error exporting data: {e}"

    def import_schedule_items_from_csv(self, file_path, work_id):
        try:
            df = pd.read_csv(file_path)
            imported_count = 0
            for index, row in df.iterrows():
                item_name = row.get('Item Name')
                quantity = row.get('Quantity')
                unit = row.get('Unit')
                parent_item_id = row.get('Parent Item ID')

                if item_name and quantity is not None and unit:
                    if pd.isna(parent_item_id):
                        parent_item_id = None

                    item_id = db_manager.add_schedule_item(
                        work_id, item_name, unit, quantity, parent_item_id
                    )
                    if item_id:
                        imported_count += 1
            return True, f"Successfully imported {imported_count} schedule items."
        except Exception as e:
            return False, f"Error importing data: {e}"

    def export_schedule_items_to_csv(self, file_path, work_id):
        try:
            schedule_items = db_manager.get_schedule_items(work_id)
            df = pd.DataFrame(schedule_items, columns=[
                'item_id', 'parent_item_id', 'item_name', 'quantity', 'unit'
            ])
            # Rename columns for clarity in the exported file
            df = df.rename(columns={
                'item_id': 'Item ID',
                'parent_item_id': 'Parent Item ID',
                'item_name': 'Item Name',
                'quantity': 'Quantity',
                'unit': 'Unit'
            })
            df.to_csv(file_path, index=False)
            return True, f"Successfully exported {len(schedule_items)} schedule items."
        except Exception as e:
            return False, f"Error exporting data: {e}"
