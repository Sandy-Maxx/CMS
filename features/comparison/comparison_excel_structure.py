
import pandas as pd

class ComparisonExcelStructure:
    def __init__(self, work_name, schedule_items, firm_names):
        self.work_name = work_name
        self.schedule_items = schedule_items
        self.firm_names = firm_names
        self.df = self._create_dataframe()

    def _create_dataframe(self):
        columns = ['Sr.No', 'Description', 'Quantity', 'Unit'] + self.firm_names
        df = pd.DataFrame(columns=columns)
        return df

    def get_dataframe(self):
        return self.df
