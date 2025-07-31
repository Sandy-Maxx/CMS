import pandas as pd
from .single_firm_data_manager import SingleFirmDataManager
from .single_firm_excel_structure import SingleFirmExcelStructure
from utils.helpers import format_currency_inr

class SingleFirmExporter:
    def __init__(self, work_id, selected_firm_name):
        self.work_id = work_id
        self.selected_firm_name = selected_firm_name
        self.data_manager = SingleFirmDataManager(work_id, selected_firm_name)
        self.excel_structure = SingleFirmExcelStructure(selected_firm_name)

    def export_to_excel(self, output_filename):
        data = self.data_manager.get_single_firm_data()
        firm_name = data['firm_name']

        header_rows = self.excel_structure.get_excel_header_structure()

        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet(firm_name)

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        data_format = workbook.add_format({
            'border': 1
        })
        currency_format = workbook.add_format({'num_format': '₹#,##,##0.00'})
        percentage_format = workbook.add_format({'num_format': '0.00%'}) 

        # Manually write multi-level headers
        self._write_multi_level_header(worksheet, header_rows, firm_name, header_format)

        # Write data rows and formulas
        data_start_row = len(header_rows) # Data starts after the header rows
        
        # Prepare data for writing, including formulas
        prepared_rows = []
        for i, item in enumerate(data['schedule_items']):
            row_data = [i + 1, item['item_name'], item['quantity']]
            
            unit_rate = item['unit_rate']
            row_data.append(unit_rate) # Unit Rate
            
            if unit_rate is not None:
                # Calculate column index for Quantity and Unit Rate for the current row
                qty_col_letter = chr(ord('A') + 2) # 'C'
                unit_rate_col_letter = chr(ord('A') + 3) # 'D'
                
                # Row index in Excel is 1-based, so add 1 to current row index + data_start_row
                excel_row_idx = data_start_row + i + 1
                
                formula = f'={qty_col_letter}{excel_row_idx}*{unit_rate_col_letter}{excel_row_idx}'
                row_data.append(formula) # Total Cost in Rs. (formula)
            else:
                row_data.append(None) # No total cost if no unit rate
            prepared_rows.append(row_data)

        # Write prepared data to worksheet
        for row_idx, row_data in enumerate(prepared_rows):
            for col_idx, cell_value in enumerate(row_data):
                if col_idx == 0 or col_idx == 1 or col_idx == 2: # SN, Description, Qty columns
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, data_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, data_format)
                elif col_idx == 3: # Unit Rate column
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, currency_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, currency_format)
                elif col_idx == 4: # Total Cost in Rs. column
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, currency_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, currency_format)

        # Add summary rows with formulas
        self._add_summary_rows_with_formulas(worksheet, data_start_row + len(prepared_rows), firm_name, header_format, currency_format, percentage_format)

        # Apply formatting
        self._apply_formatting(workbook, worksheet, self.last_data_row, currency_format, percentage_format)

        try:
            writer.close() # Use close() instead of save() for newer pandas versions
        except Exception as e:
            print(f"Error closing Excel writer: {e}")
            import traceback
            traceback.print_exc()
            raise # Re-raise the exception after logging

    def _add_summary_rows_with_formulas(self, worksheet, data_end_row, firm_name, header_format, currency_format, percentage_format):
        current_summary_row = data_end_row # This is the row index where the first summary row will start

        # Helper to get column letter from index
        def get_column_letter(col_idx):
            return chr(ord('A') + col_idx)

        # Column index for Total Cost in Rs. for the single firm is 4 (E)
        total_cost_col_idx = 4
        total_cost_col_letter = get_column_letter(total_cost_col_idx)

        # --- Total row ---
        total_row_idx = current_summary_row
        worksheet.write(total_row_idx, 1, 'Total', header_format) # Description column
        
        start_data_excel_row = len(self.excel_structure.get_excel_header_structure()) + 1
        end_data_excel_row = data_end_row # data_end_row is already 1-indexed for Excel

        formula = f'=SUM({total_cost_col_letter}{start_data_excel_row}:{total_cost_col_letter}{end_data_excel_row})'
        worksheet.write_formula(total_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- GST row ---
        gst_row_idx = current_summary_row
        worksheet.write(gst_row_idx, 1, 'GST @18%  (Rs)', header_format) # Description column
        formula = f'={total_cost_col_letter}{total_row_idx + 1}*0.18' # +1 for Excel 1-indexing
        worksheet.write_formula(gst_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Total Cost (including GST) row ---
        total_cost_gst_row_idx = current_summary_row
        worksheet.write(total_cost_gst_row_idx, 1, 'Total Cost (including GST)', header_format) # Description column
        formula = f'={total_cost_col_letter}{total_row_idx + 1}+{total_cost_col_letter}{gst_row_idx + 1}'
        worksheet.write_formula(total_cost_gst_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Rebate in % row ---
        rebate_percentage_row_idx = current_summary_row
        worksheet.write(rebate_percentage_row_idx, 1, 'Rebate in %', header_format) # Description column
        worksheet.write(rebate_percentage_row_idx, total_cost_col_idx, 0, percentage_format) # Initial value 0 for user input, apply percentage format
        current_summary_row += 1

        # --- Rebate in ₹ row ---
        rebate_amount_row_idx = current_summary_row
        worksheet.write(rebate_amount_row_idx, 1, 'Rebate in ₹', header_format) # Description column
        formula = f'={total_cost_col_letter}{total_cost_gst_row_idx + 1}*{total_cost_col_letter}{rebate_percentage_row_idx + 1}'
        worksheet.write_formula(rebate_amount_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Total after Rebate row ---
        total_after_rebate_row_idx = current_summary_row
        worksheet.write(total_after_rebate_row_idx, 1, 'Total after Rebate', header_format) # Description column
        formula = f'={total_cost_col_letter}{total_cost_gst_row_idx + 1}-{total_cost_col_letter}{rebate_amount_row_idx + 1}'
        worksheet.write_formula(total_after_rebate_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # Store the last row of data for formatting
        self.last_data_row = current_summary_row - 1 # Last row written in summary

    def _write_multi_level_header(self, worksheet, header_rows, firm_name, header_format):
        # Write first level headers
        for col_idx, cell_value in enumerate(header_rows[0]):
            if cell_value in ['SN', 'Description', 'Qty']:
                worksheet.merge_range(0, col_idx, 1, col_idx, cell_value, header_format)
            elif cell_value == firm_name:
                worksheet.merge_range(0, col_idx, 0, col_idx + 1, cell_value, header_format)

        # Write second level headers
        for col_idx, cell_value in enumerate(header_rows[1]):
            if cell_value != '': # Only write if not an empty string (already merged)
                worksheet.write(1, col_idx, cell_value, header_format)

    def _apply_formatting(self, workbook, worksheet, last_data_row, currency_format, percentage_format):
        # Set column widths for fixed columns
        worksheet.set_column(0, 0, 5)  # SN
        worksheet.set_column(1, 1, 40) # Description
        worksheet.set_column(2, 2, 15) # Qty

        # Apply column widths and currency format for firm-specific columns
        worksheet.set_column(3, 3, 15, currency_format) # Unit Rate
        worksheet.set_column(4, 4, 15, currency_format) # Total Cost

        # Rebate in % column (immediately to the right of Total Cost in Rs.)
        worksheet.set_column(5, 5, 15, percentage_format)

        # Rebate in ₹ column (immediately to the right of Rebate in %)
        worksheet.set_column(6, 6, 15, currency_format)