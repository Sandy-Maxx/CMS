from xlsxwriter.utility import xl_col_to_name

def get_vitiation_table_columns(selected_firms):
    columns = [
        ("Sr. No.", "", ""),
        ("Description", "", ""),
        ("Quantity", "Before", ""),
        ("Quantity", "After", ""),
        ("Unit", "", ""),
    ]
    for firm in selected_firms:
        columns.extend([
            (firm, "Unit Rate", ""),
            (firm, "Total Cost", "Before"),
            (firm, "Total Cost", "After"),
        ])
    return columns

def write_vitiation_excel_headers(worksheet, workbook, columns, selected_firms):
    header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

    # Create a dictionary to store merged cells for the top-level headers
    merged_cells = {}

    col_idx = 0
    for col_data in columns:
        top_header, sub_header, _ = col_data # We'll handle sub_sub_header in the third row

        # Determine span for top-level headers
        if top_header not in merged_cells:
            merged_cells[top_header] = {'start': col_idx, 'end': col_idx}
        else:
            merged_cells[top_header]['end'] = col_idx

        # Write sub-headers (row 2, 0-indexed is row 1)
        worksheet.write(1, col_idx, sub_header, header_format)

        # Write sub-sub-headers (row 3, 0-indexed is row 2) - currently empty based on your request
        # If there were specific sub-sub-headers, they would be written here.
        # For now, we'll just write an empty string with the format to maintain borders.
        worksheet.write(2, col_idx, "", header_format)

        # Set column width (adjust as needed)
        worksheet.set_column(col_idx, col_idx, 15)

        col_idx += 1

    # Merge top-level headers (row 1, 0-indexed is row 0)
    for header, span in merged_cells.items():
        start_col = span['start']
        end_col = span['end']
        if start_col != end_col:
            worksheet.merge_range(0, start_col, 0, end_col, header, header_format)
        else:
            worksheet.write(0, start_col, header, header_format)

    # Freeze the header rows
    worksheet.freeze_panes(3, 0) # Freeze rows 0, 1, 2 (3 rows) and no columns