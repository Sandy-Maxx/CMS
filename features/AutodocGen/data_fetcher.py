import sqlite3
from config import DATABASE_PATH
from database import db_manager

class DataFetcher:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_work_data(self, work_id):
        work_data = db_manager.get_work_by_id(work_id)
        return work_data

    def fetch_firms_for_work(self, work_id):
        firms = db_manager.get_unique_firm_names_by_work_id(work_id)
        return firms

    def fetch_firm_data(self, firm_name, work_id):
        # This is a simplified example. You might need to fetch more specific firm data
        # from the 'firms' table or 'firm_documents' table based on your needs.
        # For now, let's assume we can get firm document data if available.
        firm_doc_data = db_manager.get_firm_document_by_work_and_firm_name(work_id, firm_name)
        return firm_doc_data

    def fetch_all_firms_pg_details(self, work_id):
        # This fetches all firm documents for a given work_id
        # You might want to refine this to only include firms that have quoted
        # or have specific PG details.
        all_firm_docs = db_manager.get_firm_documents(work_id)
        return all_firm_docs
