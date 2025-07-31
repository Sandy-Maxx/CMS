
import pandas as pd
import os
from database import db_manager

class BulkIOManager:
    def __init__(self):
        pass

    def import_works_from_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            imported_count = 0
            for index, row in df.iterrows():
                name = row.get('Work Name')
                description = row.get('Description')
                justification = row.get('Justification')
                section = row.get('Section')
                work_type = row.get('Work Type')
                file_no = row.get('File No')
                estimate_no = row.get('Estimate No')
                tender_cost = row.get('Tender Cost')
                tender_opening_date = row.get('Tender Opening Date')
                loa_no = row.get('LOA No')
                loa_date = row.get('LOA Date')
                work_commence_date = row.get('Work Commence Date')

                if name:
                    work_id = db_manager.add_work(
                        name, description, justification, section, work_type,
                        file_no, estimate_no, tender_cost, tender_opening_date,
                        loa_no, loa_date, work_commence_date
                    )
                    if work_id:
                        imported_count += 1
            return True, f"Successfully imported {imported_count} works."
        except Exception as e:
            return False, f"Error importing data: {e}"

    def export_works_to_excel(self, file_path):
        try:
            works = db_manager.get_works()
            df = pd.DataFrame(works, columns=[
                'Work ID', 'Work Name', 'Description', 'Justification', 'Section',
                'Work Type', 'File No', 'Estimate No', 'Tender Cost',
                'Tender Opening Date', 'LOA No', 'LOA Date', 'Work Commence Date'
            ])
            df.to_excel(file_path, index=False)
            return True, f"Successfully exported {len(works)} works."
        except Exception as e:
            return False, f"Error exporting data: {e}"

    def import_works_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            imported_count = 0
            for index, row in df.iterrows():
                name = row.get('Work Name')
                description = row.get('Description')
                justification = row.get('Justification')
                section = row.get('Section')
                work_type = row.get('Work Type')
                file_no = row.get('File No')
                estimate_no = row.get('Estimate No')
                tender_cost = row.get('Tender Cost')
                tender_opening_date = row.get('Tender Opening Date')
                loa_no = row.get('LOA No')
                loa_date = row.get('LOA Date')
                work_commence_date = row.get('Work Commence Date')

                if name:
                    work_id = db_manager.add_work(
                        name, description, justification, section, work_type,
                        file_no, estimate_no, tender_cost, tender_opening_date,
                        loa_no, loa_date, work_commence_date
                    )
                    if work_id:
                        imported_count += 1
            return True, f"Successfully imported {imported_count} works."
        except Exception as e:
            return False, f"Error importing data: {e}"

    def export_works_to_csv(self, file_path):
        try:
            works = db_manager.get_works()
            df = pd.DataFrame(works, columns=[
                'Work ID', 'Work Name', 'Description', 'Justification', 'Section',
                'Work Type', 'File No', 'Estimate No', 'Tender Cost',
                'Tender Opening Date', 'LOA No', 'LOA Date', 'Work Commence Date'
            ])
            df.to_csv(file_path, index=False)
            return True, f"Successfully exported {len(works)} works."
        except Exception as e:
            return False, f"Error exporting data: {e}"
