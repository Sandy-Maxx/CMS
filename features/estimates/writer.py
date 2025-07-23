# features/estimates/writer.py

from openpyxl.utils import get_column_letter
from .constants import COLUMN_HEADERS, COLUMN_MAPPING, GST_RATE
from .utils import get_cell_reference

def write_header(worksheet):
    """
    Writes the column headers to the first row of the worksheet.
    """
    worksheet.append(COLUMN_HEADERS)
    return 1 # Returns the row index of the header

def write_work_description_row(worksheet, data_row, current_row):
    """
    Writes the special 'A' row for work description.
    """
    row_values = []
    for header in COLUMN_HEADERS:
        key = COLUMN_MAPPING.get(header)
        row_values.append(data_row.get(key))
    worksheet.append(row_values)
    return current_row + 1

def write_schedule_data_rows(worksheet, data, start_row):
    """
    Writes schedule data rows with Excel formulas.
    """
    current_row = start_row
    for item in data:
        row_values = []
        for header in COLUMN_HEADERS:
            key = COLUMN_MAPPING.get(header)
            if key == "labour_amount":
                # Qty column is 3rd (index 2), Labour rate in Rs. is 7th (index 6)
                qty_col_idx = COLUMN_HEADERS.index("Qty") + 1
                labour_rate_col_idx = COLUMN_HEADERS.index("Labour rate in Rs.") + 1
                formula = f"={get_column_letter(qty_col_idx)}{current_row}*{get_column_letter(labour_rate_col_idx)}{current_row}"
                row_values.append(formula)
            elif key == "total_in_rs":
                # Qty column is 3rd (index 2), Rate in Rs is 4th (index 3), Labour Amount is 8th (index 7)
                qty_col_idx = COLUMN_HEADERS.index("Qty") + 1
                rate_col_idx = COLUMN_HEADERS.index("Rate in Rs") + 1
                labour_amount_col_idx = COLUMN_HEADERS.index("Labour Amount") + 1
                formula = f"=({get_column_letter(qty_col_idx)}{current_row}*{get_column_letter(rate_col_idx)}{current_row})+{get_column_letter(labour_amount_col_idx)}{current_row}"
                row_values.append(formula)
            elif key == "to_be_maintained":
                qty_col_idx = COLUMN_HEADERS.index("Qty") + 1
                rate_col_idx = COLUMN_HEADERS.index("Rate in Rs") + 1
                formula = f"={get_column_letter(qty_col_idx)}{current_row}*{get_column_letter(rate_col_idx)}{current_row}"
                row_values.append(formula)
            else:
                row_values.append(item.get(key))
        worksheet.append(row_values)
        current_row += 1
    return current_row

def write_summary_section(worksheet, data_start_row, data_end_row):
    """
    Writes the summary section with formulas: Sub Total, GST, Grand Total.
    """
    current_row = data_end_row + 1

    # Sub Total
    sub_total_row = [None] * len(COLUMN_HEADERS)
    sub_total_row[COLUMN_HEADERS.index("Description")] = "Sub Total"
    total_in_rs_col_idx = COLUMN_HEADERS.index("Total in Rs") + 1
    sub_total_formula = f"=SUM({get_column_letter(total_in_rs_col_idx)}{data_start_row}:{get_column_letter(total_in_rs_col_idx)}{data_end_row})"
    sub_total_row[total_in_rs_col_idx - 1] = sub_total_formula
    worksheet.append(sub_total_row)
    sub_total_row_idx = current_row
    current_row += 1

    # GST @18%
    gst_row = [None] * len(COLUMN_HEADERS)
    gst_row[COLUMN_HEADERS.index("Description")] = f"GST @{int(GST_RATE*100)}%"
    gst_formula = f"={get_column_letter(total_in_rs_col_idx)}{sub_total_row_idx}*{GST_RATE}"
    gst_row[total_in_rs_col_idx - 1] = gst_formula
    worksheet.append(gst_row)
    gst_row_idx = current_row
    current_row += 1

    # Grand Total (All Inclusive)
    grand_total_row = [None] * len(COLUMN_HEADERS)
    grand_total_row[COLUMN_HEADERS.index("Description")] = "Grand Total (All Inclusive)"
    grand_total_formula = f"={get_column_letter(total_in_rs_col_idx)}{sub_total_row_idx}+{get_column_letter(total_in_rs_col_idx)}{gst_row_idx}"
    grand_total_row[total_in_rs_col_idx - 1] = grand_total_formula
    worksheet.append(grand_total_row)
    grand_total_row_idx = current_row
    current_row += 1

    return sub_total_row_idx, grand_total_row_idx
