from xlsxwriter.utility import xl_col_to_name

def write_vitiation_excel_headers(worksheet, workbook, selected_firms):
    header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    
    current_col = 0

    # SN (merged 3x1)
    worksheet.merge_range(0, current_col, 2, current_col, "Sr. No.", header_format)
    current_col += 1

    # Description (merged 3x1)
    worksheet.merge_range(0, current_col, 2, current_col, "Description", header_format)
    current_col += 1

    # Quantity (merged 1x3)
    qty_start_col = current_col
    worksheet.merge_range(0, qty_start_col, 0, qty_start_col + 2, "Quantity", header_format)
    worksheet.write(1, qty_start_col, "Before Variation", header_format)
    worksheet.write(1, qty_start_col + 1, "After Variation", header_format)
    worksheet.write(1, qty_start_col + 2, "Increased Qty", header_format)
    worksheet.write(2, qty_start_col, "", header_format)
    worksheet.write(2, qty_start_col + 1, "", header_format)
    worksheet.write(2, qty_start_col + 2, "", header_format)
    current_col += 3

    # Unit (merged 3x1)
    worksheet.merge_range(0, current_col, 2, current_col, "Unit", header_format)
    current_col += 1

    # Firms and their sub-headers
    for firm_name in selected_firms:
        firm_start_col = current_col
        # Firm Name (merged 1x4)
        worksheet.merge_range(0, firm_start_col, 0, firm_start_col + 3, firm_name, header_format)

        # Unit Rate (merged 2x1 vertically)
        worksheet.merge_range(1, firm_start_col, 2, firm_start_col, "Unit Rate", header_format)
        
        # Total Cost (merged 1x3 horizontally)
        total_cost_start_col = firm_start_col + 1
        worksheet.merge_range(1, total_cost_start_col, 1, total_cost_start_col + 2, "Total Cost", header_format)
        worksheet.write(2, total_cost_start_col, "Before Variation", header_format)
        worksheet.write(2, total_cost_start_col + 1, "After Variation", header_format)
        worksheet.write(2, total_cost_start_col + 2, "Increased Cost", header_format)
        
        current_col += 4 # Move to the start of the next firm's columns

    # Freeze the header rows
    worksheet.freeze_panes(3, 0) # Freeze rows 0, 1, 2 (3 rows) and no columns

    # Return the total number of columns for data alignment later
    return current_col
