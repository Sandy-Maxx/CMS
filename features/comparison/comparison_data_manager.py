
from database import db_manager

class ComparisonDataManager:
    def __init__(self, work_id):
        self.work_id = work_id

    def get_comparison_data(self):
        work_details = db_manager.get_work_by_id(self.work_id)
        schedule_items = db_manager.get_schedule_items(self.work_id)
        firm_names = db_manager.get_all_unique_firm_names()

        data = {
            'work_name': work_details['work_name'],
            'schedule_items': [],
            'firm_names': firm_names
        }

        for item in schedule_items:
            item_data = {
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'quantity': item['quantity'],
                'unit': item['unit'],
                'firm_rates': {}
            }
            firm_rates = db_manager.get_firm_rates(item['item_id'])
            for rate in firm_rates:
                item_data['firm_rates'][rate['firm_name']] = rate['unit_rate']
            data['schedule_items'].append(item_data)

        return data
