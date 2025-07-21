import sqlite3
from config import DATABASE_PATH

def create_firm_documents_table():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firm_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_id INTEGER NOT NULL,
            firm_name TEXT NOT NULL,
            pg_no TEXT,
            pg_amount REAL,
            bank_name TEXT,
            bank_address TEXT,
            firm_address TEXT,
            indemnity_bond_details TEXT,
            other_docs_details TEXT,
            submission_date TEXT,
            pg_submitted INTEGER DEFAULT 0,
            indemnity_bond_submitted INTEGER DEFAULT 0,
            FOREIGN KEY (work_id) REFERENCES works(id)
        )
    ''')
    
    # Add new columns if they don't exist
    cursor.execute("PRAGMA table_info(firm_documents)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'pg_submitted' not in columns:
        cursor.execute("ALTER TABLE firm_documents ADD COLUMN pg_submitted INTEGER DEFAULT 0")
    if 'indemnity_bond_submitted' not in columns:
        cursor.execute("ALTER TABLE firm_documents ADD COLUMN indemnity_bond_submitted INTEGER DEFAULT 0")

    cursor.execute("PRAGMA table_info(firm_documents)")
    updated_columns = [col[1] for col in cursor.fetchall()]
    print(f"Firm documents table columns after ALTER: {updated_columns}")

    conn.commit()
    conn.close()

def add_firm_document(work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO firm_documents (work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted)
    )
    conn.commit()
    conn.close()

def get_firm_documents(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted FROM firm_documents WHERE work_id = ?", (work_id,))
    documents = cursor.fetchall()
    conn.close()
    return documents

def update_firm_document(doc_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE firm_documents SET firm_name = ?, pg_no = ?, pg_amount = ?, bank_name = ?, bank_address = ?, firm_address = ?, indemnity_bond_details = ?, other_docs_details = ?, submission_date = ?, pg_submitted = ?, indemnity_bond_submitted = ? WHERE id = ?",
        (firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted, doc_id)
    )
    conn.commit()
    conn.close()

def delete_firm_document(doc_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firm_documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()
