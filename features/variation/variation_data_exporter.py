import pandas as pd
from database import db_manager
from features.variation.variation_excel_structure import get_variation_table_columns, write_variation_excel_headers
from xlsxwriter.utility import xl_col_to_name

def export_variation_data_to_excel(work_details, schedule_items, output_path, selected_firms):
    try:
        data = []
        sn_counter = 1

        for item in schedule_items:
            row_data = [
                sn_counter,
                item['item_name'],
                item['quantity'],
                item['new_quantity'],
                item['unit'],
            ]

            # Add unit rate and total costs for the selected firm
            row_data.extend([
                item['unit_rate'],
                item['total_cost_before'],
                item['total_cost_after']
            ])
            data.append(row_data)
            sn_counter += 1

        # Get the MultiIndex columns for the report
        columns = get_variation_table_columns(selected_firms)

        # Get column names to map to indices for formula generation
        # This is a flat list of the lowest level headers
        flat_columns = [col[2] if col[2] else col[1] if col[1] else col[0] for col in columns]

        # Map column names to their indices
        col_name_to_idx = {name: idx for idx, name in enumerate(flat_columns)}

        # Get the base column indices for quantities
        original_qty_col_idx = col_name_to_idx['Before Variation'] # This is the Qty Before Variation column
        new_qty_col_idx = col_name_to_idx['After Variation'] # This is the Qty After Variation column

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Variation Report')

            # Write multi-level headers
            write_variation_excel_headers(worksheet, workbook, columns, selected_firms)

            # Write data rows manually
            for row_idx, item_data in enumerate(schedule_items):
                excel_row = 3 + row_idx # Data starts at Excel row 4 (0-indexed row 3)
                cell_format = workbook.add_format({'border': 1})

                # Write SN, Schedule Items, Original Qty, New Qty, Unit
                worksheet.write(excel_row, 0, item_data['sr_no'], cell_format)
                worksheet.write(excel_row, 1, item_data['item_name'], cell_format)
                worksheet.write(excel_row, 2, item_data['quantity'], cell_format)
                worksheet.write(excel_row, 3, item_data['new_quantity'], cell_format)
                worksheet.write(excel_row, 4, item_data['unit'], cell_format)

                # Write Unit Rate, Total Cost Before, Total Cost After
                worksheet.write(excel_row, 5, item_data['unit_rate'], cell_format)
                worksheet.write(excel_row, 6, item_data['total_cost_before'], cell_format)
                worksheet.write(excel_row, 7, item_data['total_cost_after'], cell_format)

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_variation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"
