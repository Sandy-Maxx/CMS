
from database import db_manager

class ComparisonDataManager:
    def __init__(self, work_id):
        self.work_id = work_id

    def get_work_details(self):
        return db_manager.get_work_by_id(self.work_id)

    def get_schedule_items(self):
        return db_manager.get_schedule_items(self.work_id)

    def get_firm_rates(self, schedule_item_id):
        return db_manager.get_firm_rates(schedule_item_id)

    def get_all_firm_names(self):
        return db_manager.get_all_unique_firm_names()
