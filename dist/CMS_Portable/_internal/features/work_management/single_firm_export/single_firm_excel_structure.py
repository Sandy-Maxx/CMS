import pandas as pd

class SingleFirmExcelStructure:
    def __init__(self, firm_name):
        self.firm_name = firm_name

    def get_excel_header_structure(self):
        header_rows = []
        # First row (level 1)
        first_row = ['SN', 'Description', 'Qty', self.firm_name, ''] # Firm name spans two columns
        header_rows.append(first_row)

        # Second row (level 2)
        second_row = ['', '', 'No./ Lot / Set', 'Unit Rate', 'Total Cost in Rs.']
        header_rows.append(second_row)

        return header_rows

    def get_dataframe_columns(self):
        columns = ['SN', 'Description', 'Qty']
        columns.append(f'{self.firm_name} - Unit Rate')
        columns.append(f'{self.firm_name} - Total Cost in Rs.')
        
        # Add columns for Rebate and Total after Rebate
        columns.append(f'{self.firm_name} - Rebate')
        columns.append(f'{self.firm_name} - Rebate (%)')
        columns.append(f'{self.firm_name} - Total after Rebate')
        return columns
