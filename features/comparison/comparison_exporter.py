import pandas as pd
from .comparison_data_manager import ComparisonDataManager
from .comparison_excel_structure import ComparisonExcelStructure
from utils.helpers import format_currency_inr
from ..AutodocGen.data_fetcher import DataFetcher
from ..AutodocGen.pg_details_formatter import PGDetailsFormatter
from config import DATABASE_PATH

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
        percentage_format = workbook.add_format({'num_format': '0.00%'})

        # Manually write multi-level headers
        header_rows = self.excel_structure.get_excel_header_structure()
        self._write_multi_level_header(worksheet, header_rows, firm_names, header_format)

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
                if col_idx == 0 or col_idx == 1 or col_idx == 2: # SN, Description, Qty columns
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, data_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, data_format)
                elif col_idx >= 3 and (col_idx - 3) % 2 == 0: # Unit Rate column
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, currency_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, currency_format)
                elif col_idx >= 3 and (col_idx - 3) % 2 == 1: # Total Cost in Rs. column
                    if isinstance(cell_value, str) and cell_value.startswith('='):
                        worksheet.write_formula(data_start_row + row_idx, col_idx, cell_value, currency_format)
                    else:
                        worksheet.write(data_start_row + row_idx, col_idx, cell_value, currency_format)

        # Add summary rows with formulas
        firm_total_cost_col_indices = self._add_summary_rows_with_formulas(worksheet, data_start_row + len(prepared_rows), firm_names, self.excel_structure.get_dataframe_columns(), header_format, currency_format, percentage_format)

# Add PG details section
        self._add_pg_details_section(worksheet, header_format, data_format)

        # Apply formatting
        self._apply_formatting(workbook, worksheet, self.last_data_row, firm_names, firm_total_cost_col_indices, data_format, currency_format, percentage_format)

        try:
            writer.close() # Use close() instead of save() for newer pandas versions
        except Exception as e:
            print(f"Error closing Excel writer: {e}")
            import traceback
            traceback.print_exc()
            raise # Re-raise the exception after logging

    def _add_summary_rows_with_formulas(self, worksheet, data_end_row, firm_names, dataframe_columns, header_format, currency_format, percentage_format):
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
        worksheet.write(total_row_idx, 1, 'Total', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            
            # Data starts at data_start_row (0-indexed in Python) + 1 (for Excel 1-indexing)
            # and ends at data_end_row (0-indexed in Python)
            start_data_excel_row = len(self.excel_structure.get_excel_header_structure()) + 1
            end_data_excel_row = data_end_row # data_end_row is already 1-indexed for Excel

            total_cost_col_letter = get_column_letter(total_cost_col_idx)
            formula = f'=SUM({total_cost_col_letter}{start_data_excel_row}:{total_cost_col_letter}{end_data_excel_row})'
            worksheet.write_formula(total_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- GST row ---
        gst_row_idx = current_summary_row
        worksheet.write(gst_row_idx, 1, 'GST @18%  (Rs)', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cell_letter = get_column_letter(total_cost_col_idx)
            formula = f'={total_cell_letter}{total_row_idx + 1}*0.18' # +1 for Excel 1-indexing
            worksheet.write_formula(gst_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Total Cost (including GST) row ---
        total_cost_gst_row_idx = current_summary_row
        worksheet.write(total_cost_gst_row_idx, 1, 'Total Cost (including GST)', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cost_gst_cell_letter = get_column_letter(total_cost_col_idx)
            
            formula = f'={total_cost_gst_cell_letter}{total_row_idx + 1}+{total_cost_gst_cell_letter}{gst_row_idx + 1}'
            worksheet.write_formula(total_cost_gst_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Rebate in % row ---
        rebate_percentage_row_idx = current_summary_row
        worksheet.write(rebate_percentage_row_idx, 1, 'Rebate in %', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            worksheet.write(rebate_percentage_row_idx, total_cost_col_idx, 0, percentage_format) # Initial value 0 for user input, apply percentage format
        current_summary_row += 1

        # --- Rebate in ₹ row ---
        rebate_amount_row_idx = current_summary_row
        worksheet.write(rebate_amount_row_idx, 1, 'Rebate in ₹', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cost_gst_cell_letter = get_column_letter(total_cost_col_idx)
            
            # The row for Total Cost (including GST) is total_cost_gst_row_idx + 1 (Excel 1-indexed)
            # The row for Rebate in % is rebate_percentage_row_idx + 1 (Excel 1-indexed)
            formula = f'={total_cost_gst_cell_letter}{total_cost_gst_row_idx + 1}*{total_cost_gst_cell_letter}{rebate_percentage_row_idx + 1}'
            worksheet.write_formula(rebate_amount_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Total after Rebate row ---
        total_after_rebate_row_idx = current_summary_row
        worksheet.write(total_after_rebate_row_idx, 1, 'Total after Rebate', header_format) # Description column
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            total_cost_gst_cell_letter = get_column_letter(total_cost_col_idx)
            
            # The row for Total Cost (including GST) is total_cost_gst_row_idx + 1 (Excel 1-indexed)
            # The row for Rebate in ₹ is rebate_amount_row_idx + 1 (Excel 1-indexed)
            formula = f'={total_cost_gst_cell_letter}{total_cost_gst_row_idx + 1}-{total_cost_gst_cell_letter}{rebate_amount_row_idx + 1}'
            worksheet.write_formula(total_after_rebate_row_idx, total_cost_col_idx, formula, currency_format) # Apply currency format
        current_summary_row += 1

        # --- Inter se position row ---
        inter_se_row_idx = current_summary_row
        worksheet.write(inter_se_row_idx, 1, 'Inter se position', header_format) # Description column

        # Build the range string for RANK.EQ formula
        total_after_rebate_cells = []
        for firm_name in firm_names:
            col_idx = firm_total_cost_col_indices[firm_name]
            cell_ref = f'${get_column_letter(col_idx)}${total_after_rebate_row_idx + 1}'
            total_after_rebate_cells.append(cell_ref)
        rank_range_str = ','.join(total_after_rebate_cells)

        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            current_firm_total_after_rebate_cell = f'${get_column_letter(total_cost_col_idx)}${total_after_rebate_row_idx + 1}'
            
            # RANK.EQ(number, ref, [order]) - order 0 for descending (lowest value is L-1)
            # We want lowest value to be L-1, so we sort ascending and then map to L-1, L-2 etc.
            # Excel's RANK.EQ with order 0 (descending) means largest value is rank 1.
            # To get L-1 for the lowest value, we need to rank in ascending order (order 1).
            # However, the user wants L-1 for the lowest cost, so we use order 1.
            formula = f'="L-"&RANK.EQ({current_firm_total_after_rebate_cell},({rank_range_str}),1)'
            worksheet.write_formula(inter_se_row_idx, total_cost_col_idx, formula, header_format)
        current_summary_row += 1

        # Store the last row of data for formatting
        self.last_data_row = current_summary_row - 1 # Last row written in summary

        return firm_total_cost_col_indices

    def _write_multi_level_header(self, worksheet, header_rows, firm_names, header_format):
        # Write first level headers
        for col_idx, cell_value in enumerate(header_rows[0]):
            if cell_value in ['SN', 'Description', 'Qty']:
                worksheet.merge_range(0, col_idx, 1, col_idx, cell_value, header_format)
            elif cell_value in firm_names:
                # Find the next empty string to determine the merge range
                merge_end_col = col_idx
                while merge_end_col + 1 < len(header_rows[0]) and header_rows[0][merge_end_col + 1] == '':
                    merge_end_col += 1
                worksheet.merge_range(0, col_idx, 0, merge_end_col, cell_value, header_format)

        # Write second level headers
        for col_idx, cell_value in enumerate(header_rows[1]):
            if cell_value != '': # Only write if not an empty string (already merged)
                worksheet.write(1, col_idx, cell_value, header_format)

    def _apply_formatting(self, workbook, worksheet, last_data_row, firm_names, firm_total_cost_col_indices, data_format, currency_format, percentage_format):
        # Set column widths for fixed columns
        worksheet.set_column(0, 0, 5)  # SN
        worksheet.set_column(1, 1, 40) # Description
        worksheet.set_column(2, 2, 15) # Qty

        # Apply column widths and currency format for firm-specific columns
        for firm_name in firm_names:
            total_cost_col_idx = firm_total_cost_col_indices[firm_name]
            unit_rate_col_idx = total_cost_col_idx - 1 # Unit Rate is one column to the left of Total Cost

            # Unit Rate column
            worksheet.set_column(unit_rate_col_idx, unit_rate_col_idx, 15, currency_format)
            # Total Cost column
            worksheet.set_column(total_cost_col_idx, total_cost_col_idx, 15, currency_format)

            # Rebate in % column (immediately to the right of Total Cost in Rs.)
            rebate_percentage_col_idx = total_cost_col_idx + 1
            worksheet.set_column(rebate_percentage_col_idx, rebate_percentage_col_idx, 15, percentage_format)

            # Rebate in ₹ column (immediately to the right of Rebate in %)
            rebate_amount_col_idx = total_cost_col_idx + 2
            worksheet.set_column(rebate_amount_col_idx, rebate_amount_col_idx, 15, currency_format)

        # Apply formatting for Rebate in % and Rebate in ₹ rows (initial values)
        rebate_percentage_row_idx = last_data_row - 2
        rebate_amount_row_idx = last_data_row - 1
        total_after_rebate_row_idx = last_data_row

        # No need to write values here, as they are written in _add_summary_rows_with_formulas
        # This section is primarily for setting column-wide formats

        # The individual cell writes in _add_summary_rows_with_formulas already apply the header_format
        # The data_format is applied to the main data rows in export_to_excel

    def _add_pg_details_section(self, worksheet, header_format, data_format):
        """
        Add PG Details section at the bottom of the comparison table.
        """
        # Add spacing before PG details
        pg_start_row = self.last_data_row + 3
        
        # Write PG Details header
        worksheet.write(pg_start_row, 0, "Performance Guarantee Details:", header_format)
        
        # Fetch and format PG details
        data_fetcher = DataFetcher(DATABASE_PATH)
        pg_details_formatter = PGDetailsFormatter()
        pg_details = data_fetcher.fetch_all_firms_pg_details(self.work_id)
        formatted_pg_details = pg_details_formatter.format_pg_details(pg_details, self.work_id)
        
        # Split the formatted details into individual lines for better formatting
        if formatted_pg_details:
            pg_lines = formatted_pg_details.split('\n')
            current_row = pg_start_row + 1
            
            for line in pg_lines:
                if line.strip():  # Only write non-empty lines
                    worksheet.write(current_row, 0, line, data_format)
                    # Merge cells across multiple columns for better readability
                    worksheet.merge_range(current_row, 0, current_row, 5, line, data_format)
                    current_row += 1
            
            # Set row height for better visibility
            for row_idx in range(pg_start_row + 1, current_row):
                worksheet.set_row(row_idx, 25)  # Set row height to 25
        else:
            worksheet.write(pg_start_row + 1, 0, "No PG details available.", data_format)
            worksheet.merge_range(pg_start_row + 1, 0, pg_start_row + 1, 5, "No PG details available.", data_format)
