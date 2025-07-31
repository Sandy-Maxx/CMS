from database import db_manager

class SingleFirmDataManager:
    def __init__(self, work_id, selected_firm_name):
        self.work_id = work_id
        self.selected_firm_name = selected_firm_name

    def get_single_firm_data(self):
        work_details = db_manager.get_work_by_id(self.work_id)
        schedule_items = db_manager.get_schedule_items(self.work_id)

        data = {
            'work_name': work_details['work_name'],
            'schedule_items': [],
            'firm_name': self.selected_firm_name
        }

        for item in schedule_items:
            item_data = {
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'quantity': item['quantity'],
                'unit': item['unit'],
                'unit_rate': None
            }
            firm_rates = db_manager.get_firm_rates(item['item_id'])
            for rate in firm_rates:
                if rate['firm_name'] == self.selected_firm_name:
                    item_data['unit_rate'] = rate['unit_rate']
                    break
            data['schedule_items'].append(item_data)

        return data
