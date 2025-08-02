from xlsxwriter.utility import xl_col_to_name

def get_variation_table_columns():
    columns = [
        ("SN", "", ""),
        ("Schedule Items", "", ""),
        ("Quantity", "Before Variation", ""),
        ("Quantity", "After Variation", ""),
        ("Quantity", "Increased Qty", ""),
        ("Unit", "", ""),
        ("Unit Rate", "", ""),
        ("Total Cost", "Before Variation", ""),
        ("Total Cost", "After Variation", ""),
        ("Total Cost", "Increased Cost", ""),
    ]
    return columns

def write_variation_excel_report(worksheet, workbook, work_details, schedule_items, selected_firms, total_cost_before_all_items, total_cost_after_all_items, percentage_change):
    header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    data_format = workbook.add_format({'border': 1})
    currency_format = workbook.add_format({'border': 1, 'num_format': '₹ #,##0.00'})
    percentage_format = workbook.add_format({'border': 1, 'num_format': '0.00%', 'align': 'center'})
    summary_label_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'right', 'bg_color': '#D9D9D9'})
    summary_value_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '₹ #,##0.00', 'bg_color': '#D9D9D9'})
    summary_percentage_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '0.00%', 'align': 'center', 'bg_color': '#D9D9D9'})

    # Write work details
    worksheet.write('A1', 'Work Name:', header_format)
    worksheet.write('B1', work_details['work_name'], data_format)
    worksheet.write('A2', 'Selected Firm:', header_format)
    worksheet.write('B2', selected_firms[0], data_format)

    # Define columns for the table
    columns = get_variation_table_columns()

    # Create a dictionary to store merged cells to avoid re-merging
    merged_cells = {}

    col_idx = 0
    for col_data in columns:
        top_header, sub_header, sub_sub_header = col_data

        # Determine span for top-level headers
        if top_header not in merged_cells:
            merged_cells[top_header] = {'start': col_idx, 'end': col_idx}
        else:
            merged_cells[top_header]['end'] = col_idx

        # Write sub-headers (row 2, 0-indexed is row 1)
        worksheet.write(4, col_idx, sub_header, header_format)

        # Write sub-sub-headers (row 3, 0-indexed is row 2) - currently empty based on your request
        worksheet.write(5, col_idx, sub_sub_header, header_format)

        # Set column width (adjust as needed)
        worksheet.set_column(col_idx, col_idx, 15)

        col_idx += 1

    # Merge top-level headers (row 1, 0-indexed is row 0)
    for header, span in merged_cells.items():
        start_col = span['start']
        end_col = span['end']
        if start_col != end_col:
            worksheet.merge_range(3, start_col, 3, end_col, header, header_format)
        else:
            worksheet.write(3, start_col, header, header_format)

    # Freeze the header rows
    worksheet.freeze_panes(6, 0) # Freeze rows 0-5 (6 rows) and no columns

    # Write data rows
    start_row_data = 6 # Data starts at Excel row 7 (0-indexed row 6)
    for row_idx, item_data in enumerate(schedule_items):
        excel_row = start_row_data + row_idx

        worksheet.write(excel_row, 0, item_data['sr_no'], data_format)  # SN
        worksheet.write(excel_row, 1, item_data['item_name'], data_format)  # Schedule Items
        worksheet.write(excel_row, 2, item_data['quantity'], data_format)  # Qty Before Variation
        worksheet.write(excel_row, 3, item_data['new_quantity'], data_format)  # Qty After Variation
        # Increased Qty formula: After - Before
        formula_increased_qty = f"={xl_col_to_name(3)}{excel_row+1}-{xl_col_to_name(2)}{excel_row+1}"
        worksheet.write_formula(excel_row, 4, formula_increased_qty, data_format)  # Increased Qty
        worksheet.write(excel_row, 5, item_data['unit'], data_format)  # Unit
        worksheet.write(excel_row, 6, item_data['unit_rate'], currency_format)  # Unit Rate
        # Total Cost Before = Qty Before * Unit Rate
        formula_total_cost_before = f"={xl_col_to_name(2)}{excel_row+1}*{xl_col_to_name(6)}{excel_row+1}"
        worksheet.write_formula(excel_row, 7, formula_total_cost_before, currency_format)  # Total Cost Before
        # Total Cost After = Qty After * Unit Rate
        formula_total_cost_after = f"={xl_col_to_name(3)}{excel_row+1}*{xl_col_to_name(6)}{excel_row+1}"
        worksheet.write_formula(excel_row, 8, formula_total_cost_after, currency_format)  # Total Cost After
        # Increased Cost = Total Cost After - Total Cost Before
        formula_increased_cost = f"={xl_col_to_name(8)}{excel_row+1}-{xl_col_to_name(7)}{excel_row+1}"
        worksheet.write_formula(excel_row, 9, formula_increased_cost, currency_format)  # Increased Cost

    # Write summary rows
    summary_row_start = start_row_data + len(schedule_items) + 1 # Add an empty row for spacing

    COL_TOTAL_COST_BEFORE = 7  # Updated column index
    COL_TOTAL_COST_AFTER = 8   # Updated column index  
    COL_INCREASED_COST = 9     # New column index
    COL_LABEL_START = 0
    COL_LABEL_END = 6          # Updated to cover up to Unit Rate column

    # Subtotal row - single row with values in all three cost columns
    subtotal_row = summary_row_start
    worksheet.merge_range(subtotal_row, COL_LABEL_START, subtotal_row, COL_LABEL_END, 'Subtotal:', summary_label_format)
    
    # Subtotal Before Variation
    formula_subtotal_before = f"=SUM({xl_col_to_name(COL_TOTAL_COST_BEFORE)}{start_row_data+1}:{xl_col_to_name(COL_TOTAL_COST_BEFORE)}{start_row_data + len(schedule_items)})"
    worksheet.write_formula(subtotal_row, COL_TOTAL_COST_BEFORE, formula_subtotal_before, summary_value_format)
    
    # Subtotal After Variation
    formula_subtotal_after = f"=SUM({xl_col_to_name(COL_TOTAL_COST_AFTER)}{start_row_data+1}:{xl_col_to_name(COL_TOTAL_COST_AFTER)}{start_row_data + len(schedule_items)})"
    worksheet.write_formula(subtotal_row, COL_TOTAL_COST_AFTER, formula_subtotal_after, summary_value_format)
    
    # Subtotal Increased Cost
    formula_subtotal_increased = f"=SUM({xl_col_to_name(COL_INCREASED_COST)}{start_row_data+1}:{xl_col_to_name(COL_INCREASED_COST)}{start_row_data + len(schedule_items)})"
    worksheet.write_formula(subtotal_row, COL_INCREASED_COST, formula_subtotal_increased, summary_value_format)

    # GST @ 18% row - single row with values in all three cost columns
    gst_rate = 0.18
    gst_row = subtotal_row + 1
    worksheet.merge_range(gst_row, COL_LABEL_START, gst_row, COL_LABEL_END, f'GST @ {gst_rate*100:.0f}%:', summary_label_format)
    
    # GST Before Variation
    formula_gst_before = f"={xl_col_to_name(COL_TOTAL_COST_BEFORE)}{subtotal_row+1}*{gst_rate}"
    worksheet.write_formula(gst_row, COL_TOTAL_COST_BEFORE, formula_gst_before, summary_value_format)
    
    # GST After Variation
    formula_gst_after = f"={xl_col_to_name(COL_TOTAL_COST_AFTER)}{subtotal_row+1}*{gst_rate}"
    worksheet.write_formula(gst_row, COL_TOTAL_COST_AFTER, formula_gst_after, summary_value_format)
    
    # GST Increased Cost
    formula_gst_increased = f"={xl_col_to_name(COL_INCREASED_COST)}{subtotal_row+1}*{gst_rate}"
    worksheet.write_formula(gst_row, COL_INCREASED_COST, formula_gst_increased, summary_value_format)

    # Total Cost (including GST) row - single row with values in all three cost columns
    total_gst_row = gst_row + 1
    worksheet.merge_range(total_gst_row, COL_LABEL_START, total_gst_row, COL_LABEL_END, 'Total Cost (with GST):', summary_label_format)
    
    # Total Cost Before Variation (with GST)
    formula_total_before_gst = f"={xl_col_to_name(COL_TOTAL_COST_BEFORE)}{subtotal_row+1}+{xl_col_to_name(COL_TOTAL_COST_BEFORE)}{gst_row+1}"
    worksheet.write_formula(total_gst_row, COL_TOTAL_COST_BEFORE, formula_total_before_gst, summary_value_format)
    
    # Total Cost After Variation (with GST)
    formula_total_after_gst = f"={xl_col_to_name(COL_TOTAL_COST_AFTER)}{subtotal_row+1}+{xl_col_to_name(COL_TOTAL_COST_AFTER)}{gst_row+1}"
    worksheet.write_formula(total_gst_row, COL_TOTAL_COST_AFTER, formula_total_after_gst, summary_value_format)
    
    # Total Increased Cost (with GST)
    formula_total_increased_gst = f"={xl_col_to_name(COL_INCREASED_COST)}{subtotal_row+1}+{xl_col_to_name(COL_INCREASED_COST)}{gst_row+1}"
    worksheet.write_formula(total_gst_row, COL_INCREASED_COST, formula_total_increased_gst, summary_value_format)

    # Percentage Change row
    percentage_change_row = total_gst_row + 1
    worksheet.merge_range(percentage_change_row, COL_LABEL_START, percentage_change_row, COL_LABEL_END, 'Percentage Change:', summary_label_format)
    formula_percentage_change = f"=(({xl_col_to_name(COL_TOTAL_COST_AFTER)}{total_gst_row+1}-{xl_col_to_name(COL_TOTAL_COST_BEFORE)}{total_gst_row+1})/{xl_col_to_name(COL_TOTAL_COST_BEFORE)}{total_gst_row+1})"
    worksheet.write_formula(percentage_change_row, COL_INCREASED_COST, formula_percentage_change, summary_percentage_format)

    