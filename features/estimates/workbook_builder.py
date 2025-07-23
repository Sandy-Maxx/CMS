# features/estimates/workbook_builder.py

from openpyxl import Workbook

def create_workbook_and_sheet():
    """
    Creates a new Excel workbook and a worksheet.
    """
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Estimate Report"
    return workbook, worksheet
