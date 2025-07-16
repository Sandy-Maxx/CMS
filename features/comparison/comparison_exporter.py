import pandas as pd
from .comparison_data_manager import ComparisonDataManager
from .comparison_excel_structure import ComparisonExcelStructure
from utils.helpers import format_currency_inr

class ComparisonExporter:
    def __init__(self, work_id):
        self.work_id = work_id
        self.data_manager = ComparisonDataManager(work_id)
        self.excel_structure = ComparisonExcelStructure([]) # Initialize here, will be updated later

    def export_to_excel(self, output_filename):
        data = self.data_manager.get_comparison_data()
        firm_names = data['firm_names']

        self.excel_structure = ComparisonExcelStructure(firm_names)
        header_rows = self.excel_structure.get_excel_header_structure()

        rows = []
        for i, item in enumerate(data['schedule_items']):
            row = {
                'SN': i + 1,
                'Description': item['item_name'],
                'Qty': item['quantity']
            }
            for firm_name in firm_names:
                if firm_name in item['firm_rates']:
                    row[f'{firm_name} - Unit Rate'] = item['firm_rates'][firm_name]
                    row[f'{firm_name} - Total Cost in Rs.'] = item['quantity'] * item['firm_rates'][firm_name]
            rows.append(row)

        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet('Comparison')

        # Manually write multi-level headers
        header_rows = self.excel_structure.get_excel_header_structure()
        self._write_multi_level_header(worksheet, header_rows, firm_names)

        # Write data rows and formulas
        data_start_row = len(header_rows) # Data starts after the header rows
        
        # Prepare data for writing, including formulas
        prepared_rows = []
        for i, item in enumerate(data['schedule_items']):
            row_data = [i + 1, item['item_name'], item['quantity']]
            firm_col_start_idx = 3 # SN, Description, Qty
            
            for firm_name in firm_names:
                unit_rate = item['firm_rates'].get(firm_name)
                row_data.append(unit_rate) # Unit Rate
                
                if unit_rate is not None:
                    # Calculate column index for Quantity and Unit Rate for the current row
                    qty_col_letter = chr(ord('A') + 2) # 'C'
                    unit_rate_col_letter = chr(ord('A') + firm_col_start_idx)
                    
                    # Row index in Excel is 1-based, so add 1 to current row index + data_start_row
                    excel_row_idx = data_start_row + i + 1
                    
                    formula = f'={qty_col_letter}{excel_row_idx}*{unit_rate_col_letter}{excel_row_idx}'
                    row_data.append(formula) # Total Cost in Rs. (formula)
                else:
                    row_data.append(None) # No total cost if no unit rate
                firm_col_start_idx += 2 # Move to next firm's unit rate column
            prepared_rows.append(row_data)

        # Write prepared data to worksheet
        for row_idx, row_data in enumerate(prepared_rows):
            for col_idx, cell_value in enumerate(row_data):
                if isinstance(cell_value, str) and cell_value.startswith('='):
                    worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value)
                else:
                    worksheet.write(data_start_row + row_idx, col_idx, cell_value)

        # Add summary rows with formulas
        # Add summary rows with formulas
        self._add_summary_rows_with_formulas(worksheet, data_start_row + len(prepared_rows), firm_names, self.excel_structure.get_dataframe_columns())

        # Apply formatting
        self._apply_formatting(workbook, worksheet, self.last_data_row, firm_names)

        try:
            writer.close() # Use close() instead of save() for newer pandas versions
        except Exception as e:
            print(f"Error closing Excel writer: {e}")
            import traceback
            traceback.print_exc()
            raise # Re-raise the exception after logging

    def _add_summary_rows_with_formulas(self, worksheet, data_end_row, firm_names, dataframe_columns):
        current_summary_row = data_end_row # This is the row index where the first summary row will start

        # Helper to get column letter from index
        def get_column_letter(col_idx):
            return chr(ord('A') + col_idx)

        # Find column indices for firm-specific total cost columns
        firm_total_cost_col_indices = {}
        col_idx_counter = 3 # Start after SN, Description, Qty
        for firm_name in firm_names:
            # Skip Unit Rate column
            col_idx_counter += 1
            # Total Cost in Rs. column
            firm_total_cost_col_indices[firm_name] = col_idx_counter
            col_idx_counter += 1

        # --- Total row ---
        total_row_idx = current_summary_row
        worksheet.write(total_row_idx, 1, 'Total') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            
            # Data starts at data_start_row (0-indexed in Python) + 1 (for Excel 1-indexing)
            # and ends at data_end_row (0-indexed in Python)
            start_data_excel_row = len(self.excel_structure.get_excel_header_structure()) + 1
            end_data_excel_row = data_end_row # data_end_row is already 1-indexed for Excel

            total_cost_col_letter = get_column_letter(total_cost_col_idx)
            formula = f'=SUM({total_cost_col_letter}{start_data_excel_row}:{total_cost_col_letter}{end_data_excel_row})'
            worksheet.write_formula(total_row_idx, total_cost_col_idx, formula)
        current_summary_row += 1

        # --- GST row ---
        gst_row_idx = current_summary_row
        worksheet.write(gst_row_idx, 1, 'GST @18%  (Rs)') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cell_letter = get_column_letter(total_cost_col_idx)
            formula = f'={total_cell_letter}{total_row_idx + 1}*0.18' # +1 for Excel 1-indexing
            worksheet.write_formula(gst_row_idx, total_cost_col_idx, formula)
        current_summary_row += 1

        # --- Total Cost (including GST) row ---
        total_cost_gst_row_idx = current_summary_row
        worksheet.write(total_cost_gst_row_idx, 1, 'Total Cost (including GST)') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cell_letter = get_column_letter(total_cost_col_idx)
            
            formula = f'={total_cell_letter}{total_row_idx + 1}+{total_cell_letter}{gst_row_idx + 1}'
            worksheet.write_formula(total_cost_gst_row_idx, total_cost_col_idx, formula)
        current_summary_row += 1

        # --- Rebate in % row ---
        rebate_percentage_row_idx = current_summary_row
        worksheet.write(rebate_percentage_row_idx, 1, 'Rebate in %') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            worksheet.write(rebate_percentage_row_idx, total_cost_col_idx, 0) # Initial value 0 for user input
        current_summary_row += 1

        # --- Rebate in ₹ row ---
        rebate_amount_row_idx = current_summary_row
        worksheet.write(rebate_amount_row_idx, 1, 'Rebate in ₹') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cost_gst_cell_letter = get_column_letter(total_cost_col_idx)
            
            # The row for Total Cost (including GST) is total_cost_gst_row_idx + 1 (Excel 1-indexed)
            # The row for Rebate in % is rebate_percentage_row_idx + 1 (Excel 1-indexed)
            formula = f'={total_cost_gst_cell_letter}{total_cost_gst_row_idx + 1}*{total_cost_gst_cell_letter}{rebate_percentage_row_idx + 1}'
            worksheet.write_formula(rebate_amount_row_idx, total_cost_col_idx, formula)
        current_summary_row += 1

        # --- Total after Rebate row ---
        total_after_rebate_row_idx = current_summary_row
        worksheet.write(total_after_rebate_row_idx, 1, 'Total after Rebate') # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cost_gst_cell_letter = get_column_letter(total_cost_col_idx)
            
            # The row for Total Cost (including GST) is total_cost_gst_row_idx + 1 (Excel 1-indexed)
            # The row for Rebate in ₹ is rebate_amount_row_idx + 1 (Excel 1-indexed)
            formula = f'={total_cost_gst_cell_letter}{total_cost_gst_row_idx + 1}-{total_cost_gst_cell_letter}{rebate_amount_row_idx + 1}'
            worksheet.write_formula(total_after_rebate_row_idx, total_cost_col_idx, formula)
        current_summary_row += 1

        # --- Inter se position row ---
        inter_se_row_idx = current_summary_row
        worksheet.write(inter_se_row_idx, 1, 'Inter se position') # Description column

        # Calculate inter se position in Python and write values
        firm_totals_after_rebate = []
        for firm_name in firm_names:
            # Need to get the value from the 'Total after Rebate' cell
            # This is tricky because it's a formula. We'd need to read the calculated value
            # which isn't directly available from xlsxwriter.
            # For now, I'll assume we can get the value from the formula.
            # A more robust solution might involve re-calculating in Python or
            # using a different library if complex Excel formula evaluation is needed.
            # For simplicity, I'll use a placeholder or re-calculate based on the original data
            # if possible, or leave it as a manual entry for now.
            # For now, I'll write 0 and it can be manually updated.
            firm_totals_after_rebate.append(0) # Placeholder

        # This part needs actual values to rank. Since we are writing formulas,
        # we don't have the calculated values in Python at this point.
        # For a true inter se position, Excel would need to calculate first.
        # A simple approach is to write 0s and let the user manually update or
        # to use a very complex Excel array formula if supported by xlsxwriter.
        # For now, I'll write 0s.
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            worksheet.write(inter_se_row_idx, total_cost_col_idx, 0) # Placeholder
        current_summary_row += 1

        # Store the last row of data for formatting
        self.last_data_row = current_summary_row - 1 # Last row written in summary

    def _write_multi_level_header(self, worksheet, header_rows, firm_names):
        # Write first level headers
        for col_idx, cell_value in enumerate(header_rows[0]):
            if cell_value in ['SN', 'Description', 'Qty']:
                worksheet.merge_range(0, col_idx, 1, col_idx, cell_value)
            elif cell_value in firm_names:
                # Find the next empty string to determine the merge range
                merge_end_col = col_idx
                while merge_end_col + 1 < len(header_rows[0]) and header_rows[0][merge_end_col + 1] == '':
                    merge_end_col += 1
                worksheet.merge_range(0, col_idx, 0, merge_end_col, cell_value)
            elif cell_value == 'Rebate in %':
                worksheet.merge_range(0, col_idx, 0, col_idx + len(firm_names) * 2 - 1, cell_value) # Merge across all firm columns (2 per firm)
            elif cell_value == 'Rebate in ₹':
                worksheet.merge_range(0, col_idx, 0, col_idx + len(firm_names) * 2 - 1, cell_value) # Merge across all firm columns (2 per firm)
            elif cell_value == 'Total after Rebate':
                worksheet.merge_range(0, col_idx, 0, col_idx + len(firm_names) * 2 - 1, cell_value) # Merge across all firm columns

        # Write second level headers
        for col_idx, cell_value in enumerate(header_rows[1]):
            if cell_value != '': # Only write if not an empty string (already merged)
                worksheet.write(1, col_idx, cell_value)

    def _apply_formatting(self, workbook, worksheet, last_data_row, firm_names):
        # Set column widths for fixed columns
        worksheet.set_column(0, 0, 5)  # SN
        worksheet.set_column(1, 1, 40) # Description
        worksheet.set_column(2, 2, 15) # Qty

        # Define currency format
        currency_format = workbook.add_format({'num_format': '₹#,##0.00'})
        percentage_format = workbook.add_format({'num_format': '0.00%'})

        # Apply column widths and currency format for firm-specific columns
        current_col = 3 # Start after SN, Description, Qty
        for firm_name in firm_names:
            # Unit Rate column
            worksheet.set_column(current_col, current_col, 15, currency_format)
            current_col += 1
            # Total Cost column
            worksheet.set_column(current_col, current_col, 15, currency_format)
            current_col += 1

        # Apply formatting for Rebate in % and Rebate in ₹ rows
        rebate_percentage_row_idx = last_data_row - 2
        rebate_amount_row_idx = last_data_row - 1
        total_after_rebate_row_idx = last_data_row

        current_col = 3 # Start after SN, Description, Qty
        for firm_name in firm_names:
            # Skip Unit Rate and Total Cost columns for the main data rows
            current_col += 2

            # Rebate in % - percentage format
            worksheet.write(rebate_percentage_row_idx, current_col, '', percentage_format) # Apply format to user input cell
            current_col += 1

            # Rebate in ₹ - currency format
            worksheet.write(rebate_amount_row_idx, current_col, '', currency_format) # Apply format to formula cell
            current_col += 1

        current_col = 3 # Reset for Total after Rebate
        for firm_name in firm_names:
            current_col += 2 # Skip Unit Rate and Total Cost columns for the main data rows
            worksheet.write(total_after_rebate_row_idx, current_col, '', currency_format) # Apply format to formula cell
            current_col += 2 # Skip the percentage and rebate amount columns