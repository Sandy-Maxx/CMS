# features/estimates/export_runner.py

import os
import sys
from datetime import datetime
from .data_loader import load_data
from .workbook_builder import create_workbook_and_sheet
from .writer import write_header, write_work_description_row, write_schedule_data_rows, write_summary_section, write_work_name_row
from .formatter import apply_all_styles_and_formats
from .header_writer import write_estimate_header_block_simple
from .constants import COLUMN_HEADERS

def run_export(work_id, firm_name, estimate_no=None, work_subcategory=None):
    """
    Main script to trigger the export and save the Excel file.
    
    Args:
        work_id: The work ID to export
        firm_name: The firm name to export
        estimate_no: The estimate number to display in the header (optional)
        work_subcategory: The work subcategory ('M&P', 'RSP', or None) for allocation code selection (optional)
    """
    data, extracted_subcategory = load_data(work_id, firm_name)
    if not data:
        print("No data to export.")
        return
    
    # Use extracted subcategory from work metadata, fallback to passed parameter
    final_subcategory = extracted_subcategory if extracted_subcategory else work_subcategory

    workbook, worksheet = create_workbook_and_sheet()

    # Write estimate header block first
    current_row = write_estimate_header_block_simple(worksheet, estimate_no if estimate_no else "[ESTIMATE_NO]")

    # Write work description row (the 'A' row)
    work_description_data = data[0] # Assuming the first record is the 'A' row

    # Write work name row, then header, then description row
    work_name_row_idx = current_row  # Start after header block
    current_row = write_work_name_row(worksheet, work_description_data, work_name_row_idx)
    header_row_idx = write_header(worksheet, work_description_data, current_row)
    current_row = write_work_description_row(worksheet, work_description_data, header_row_idx + 1)

    # Write schedule data rows
    data_start_row = current_row
    schedule_data = data[1:] # All data except the first (A) row
    data_end_row = write_schedule_data_rows(worksheet, schedule_data, data_start_row) -1 # -1 because write_schedule_data_rows returns the next available row

    # Write summary section
    summary_start_row, summary_end_row = write_summary_section(worksheet, data_start_row, data_end_row, final_subcategory)

    # Apply styles and formats
    apply_all_styles_and_formats(worksheet, header_row_idx, data_start_row, data_end_row, summary_start_row, summary_end_row, COLUMN_HEADERS, data, work_name_row_idx)

    # Determine output directory and filename
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        application_path = os.path.dirname(sys.executable)
    else:
        # Running in a normal Python environment
        application_path = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(application_path, "exported") # Construct path relative to executable
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


