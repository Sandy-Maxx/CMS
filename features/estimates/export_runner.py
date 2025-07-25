# features/estimates/export_runner.py

import os
from datetime import datetime
from .data_loader import load_data
from .workbook_builder import create_workbook_and_sheet
from .writer import write_header, write_work_description_row, write_schedule_data_rows, write_summary_section
from .formatter import apply_all_styles_and_formats
from .constants import COLUMN_HEADERS

def run_export(work_id, firm_name):
    """
    Main script to trigger the export and save the Excel file.
    """
    data = load_data(work_id, firm_name)
    if not data:
        print("No data to export.")
        return

    workbook, worksheet = create_workbook_and_sheet()

    # Write work description row (the 'A' row)
    work_description_data = data[0] # Assuming the first record is the 'A' row

    # Write header
    header_row_idx = write_header(worksheet, work_description_data)
    current_row = write_work_description_row(worksheet, work_description_data, header_row_idx + 1)

    # Write schedule data rows
    data_start_row = current_row
    schedule_data = data[1:] # All data except the first (A) row
    data_end_row = write_schedule_data_rows(worksheet, schedule_data, data_start_row) -1 # -1 because write_schedule_data_rows returns the next available row

    # Write summary section
    summary_start_row, summary_end_row = write_summary_section(worksheet, data_start_row, data_end_row)

    # Apply styles and formats
    apply_all_styles_and_formats(worksheet, header_row_idx, data_start_row, data_end_row, summary_start_row, summary_end_row, COLUMN_HEADERS, data)

    # Determine output directory and filename
    output_dir = "exported"
    os.makedirs(output_dir, exist_ok=True)

    # Get work name from the description of the 'A' row
    work_name = _sanitize_filename(work_description_data.get("description", "Untitled_Work"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{work_name}_estimate_{timestamp}.xlsx"
    file_path = os.path.join(output_dir, filename)

    # Save the workbook
    workbook.save(file_path)
    print(f"Estimate report saved to {file_path}")


def _sanitize_filename(filename):
    """
    Sanitizes a string to be safe for use as a filename.
    Removes or replaces characters that are invalid in Windows filenames.
    """
    # Invalid characters for Windows filenames: < > : " / \ | ? *
    # Also control characters (0-31)
    invalid_chars = '< > : " / \\ | ? *' + '\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\t\n\u000b\u000c\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


