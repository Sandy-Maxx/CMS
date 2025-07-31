
import pandas as pd

class ComparisonExcelStructure:
    def __init__(self, firm_names):
        self.firm_names = firm_names

    def get_excel_header_structure(self):
        # Returns the structure for manual Excel header writing (two rows)
        header_rows = []
        # First row (level 1)
        first_row = ['SN', 'Description', 'Qty']
        for firm_name in self.firm_names:
            first_row.extend([firm_name, '']) # Firm name spans two columns
        header_rows.append(first_row)

        # Second row (level 2)
        second_row = ['', '', 'No./ Lot / Set']
        for _ in self.firm_names:
            second_row.extend(['Unit Rate', 'Total Cost in Rs.'])
        header_rows.append(second_row)

        return header_rows

    def get_dataframe_columns(self):
        # Returns a flattened list of column names for the pandas DataFrame
        columns = ['SN', 'Description', 'Qty']
        for firm_name in self.firm_names:
            columns.append(f'{firm_name} - Unit Rate')
            columns.append(f'{firm_name} - Total Cost in Rs.')
        
        # Add columns for Rebate and Total after Rebate
        for firm_name in self.firm_names:
            columns.append(f'{firm_name} - Rebate')
            columns.append(f'{firm_name} - Rebate (%)')
        for firm_name in self.firm_names:
            columns.append(f'{firm_name} - Total after Rebate')
        return columns
