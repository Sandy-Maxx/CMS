import pandas as pd
from .comparison_data_manager import ComparisonDataManager
from .comparison_excel_structure import ComparisonExcelStructure
from utils.helpers import format_currency_inr

class ComparisonExporter:
    def __init__(self, work_id):
        self.work_id = work_id
        self.data_manager = ComparisonDataManager(work_id)

    def export_to_excel(self, output_filename):
        data = self.data_manager.get_comparison_data()
        firm_names = data['firm_names']

        excel_structure = ComparisonExcelStructure(firm_names)
        header_rows = excel_structure.get_excel_header_structure()

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

        df = pd.DataFrame(rows, columns=excel_structure.get_dataframe_columns())

        df = self._add_summary_rows(df, firm_names)

        writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet('Comparison')

        # Manually write multi-level headers
        header_rows = excel_structure.get_excel_header_structure()
        self._write_multi_level_header(worksheet, header_rows, firm_names)

        # Write DataFrame data starting after the headers
        data_start_row = len(header_rows) # Data starts after the header rows
        df.to_excel(writer, sheet_name='Comparison', index=False, header=False, startrow=data_start_row)

        # Apply formatting
        self._apply_formatting(workbook, worksheet, df, firm_names)

        try:
            writer.close() # Use close() instead of save() for newer pandas versions
        except Exception as e:
            print(f"Error closing Excel writer: {e}")
            import traceback
            traceback.print_exc()
            raise # Re-raise the exception after logging

    def _add_summary_rows(self, df, firm_names):
        # Total row
        total_row = {'Description': 'Total'}
        for firm_name in firm_names:
            total_row[f'{firm_name} - Total Cost in Rs.'] = df[f'{firm_name} - Total Cost in Rs.'].sum()
        df = pd.concat([df, pd.DataFrame([total_row], columns=df.columns)], ignore_index=True)

        # GST row
        gst_row = {'Description': 'GST @18%  (Rs)'}
        for firm_name in firm_names:
            gst_row[f'{firm_name} - Total Cost in Rs.'] = df[f'{firm_name} - Total Cost in Rs.'].iloc[-1] * 0.18
        df = pd.concat([df, pd.DataFrame([gst_row], columns=df.columns)], ignore_index=True)

        # Total cost row
        total_cost_row = {('Description', ''): 'Total Cost (All Inclusive)   (Rs)'}
        for firm_name in firm_names:
            total_cost_row[f'{firm_name} - Total Cost in Rs.'] = df[f'{firm_name} - Total Cost in Rs.'].iloc[-2] + df[f'{firm_name} - Total Cost in Rs.'].iloc[-1]
        df = pd.concat([df, pd.DataFrame([total_cost_row], columns=df.columns)], ignore_index=True)

        # Inter se position row
        inter_se_row = {('Description', ''): 'Inter se position'}
        firm_totals = [df[f'{firm_name} - Total Cost in Rs.'].iloc[-1] for firm_name in firm_names]
        sorted_firm_totals = sorted(firm_totals)
        for firm_name in firm_names:
            inter_se_row[f'{firm_name} - Total Cost in Rs.'] = sorted_firm_totals.index(df[f'{firm_name} - Total Cost in Rs.'].iloc[-1]) + 1
        df = pd.concat([df, pd.DataFrame([inter_se_row], columns=df.columns)], ignore_index=True)

        return df

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

        # Write second level headers
        for col_idx, cell_value in enumerate(header_rows[1]):
            if cell_value != '': # Only write if not an empty string (already merged)
                worksheet.write(1, col_idx, cell_value)

    def _apply_formatting(self, workbook, worksheet, df, firm_names):
        # Set column widths for fixed columns
        worksheet.set_column(0, 0, 5)  # SN
        worksheet.set_column(1, 1, 40) # Description
        worksheet.set_column(2, 2, 15) # Qty

        # Define currency format
        currency_format = workbook.add_format({'num_format': '₹#,##0.00'})

        # Apply column widths and currency format for firm-specific columns
        current_col = 3 # Start after SN, Description, Qty
        for firm_name in firm_names:
            # Unit Rate column
            worksheet.set_column(current_col, current_col, 15, currency_format)
            current_col += 1
            # Total Cost column
            worksheet.set_column(current_col, current_col, 15, currency_format)
            current_col += 1