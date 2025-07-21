from database import db_manager

class WorkDataProvider:
    def __init__(self, work_id):
        self.work_id = work_id
        self.work_details = db_manager.get_work_by_id(work_id)

    def get_data(self, placeholder):
        if self.work_details and placeholder in self.work_details:
            return self.work_details[placeholder]
        return f"[Invalid Work Data Placeholder: {placeholder}]"

    def get_firm_document_data(self, firm_name):
        # Assuming there's a function in db_manager to get firm documents by work_id and firm_name
        # This might need to be added to db_manager if it doesn't exist
        firm_docs = db_manager.get_firm_documents(self.work_id) # This gets all firm docs for the work
        for doc in firm_docs:
            if doc[2] == firm_name: # firm_name is at index 2 in the tuple
                # Convert tuple to dictionary for easier access
                # This assumes the order of columns in get_firm_documents matches the table schema
                return {
                    'id': doc[0],
                    'work_id': doc[1],
                    'firm_name': doc[2],
                    'pg_no': doc[3],
                    'pg_amount': doc[4],
                    'bank_name': doc[5],
                    'bank_address': doc[6],
                    'firm_address': doc[7],
                    'indemnity_bond_details': doc[8],
                    'other_docs_details': doc[9],
                    'submission_date': doc[10],
                    'pg_submitted': doc[11],
                    'indemnity_bond_submitted': doc[12]
                }
        return None

    def get_firm_names_list(self):
        # This function should return a comma-separated string of firm names
        # associated with the current work_id. You might need to implement
        # a new function in db_manager for this, or adapt an existing one.
        # For now, I'll use get_unique_firm_names_by_work_id and join them.
        firm_names = db_manager.get_unique_firm_names_by_work_id(self.work_id)
        return ', '.join(firm_names)
