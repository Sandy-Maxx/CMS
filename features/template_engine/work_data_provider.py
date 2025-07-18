from database import db_manager

class WorkDataProvider:
    def __init__(self, work_id):
        self.work_id = work_id

    def get_data(self, placeholder):
        if placeholder == 'work_name':
            return self.get_work_name()
        elif placeholder == 'justification':
            return self.get_justification()
        # Add more placeholders here
        else:
            return f"[Invalid Placeholder: {placeholder}]"

    def get_work_name(self):
        work = db_manager.get_work_by_id(self.work_id)
        return work['work_name'] if work else ''

    def get_justification(self):
        work = db_manager.get_work_by_id(self.work_id)
        return work['justification'] if work else ''