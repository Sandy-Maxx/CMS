import sqlite3
from config import DATABASE_PATH

def create_firm_documents_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firm_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_id INTEGER,
            firm_name TEXT,
            pg_type TEXT,
            pg_no TEXT,
            pg_amount REAL,
            pg_submitted_on TEXT,
            pg_vetted_on TEXT,
            bank_name TEXT,
            bank_address TEXT,
            firm_address TEXT,
            indemnity_bond_details TEXT,
            indemnity_submitted_on TEXT,
            indemnity_vetted_on TEXT,
            other_docs_details TEXT,
            submission_date TEXT,
            pg_submitted INTEGER,
            indemnity_bond_submitted INTEGER,
            FOREIGN KEY (work_id) REFERENCES works(id),
            UNIQUE(work_id, firm_name)
        )
    """)

    # Add new columns to firm_documents if they don't exist (for backward compatibility)
    firm_documents_columns_to_add = {
        "pg_type": "TEXT",
        "pg_submitted_on": "TEXT",
        "pg_vetted_on": "TEXT",
        "indemnity_submitted_on": "TEXT",
        "indemnity_vetted_on": "TEXT"
    }

    for column, col_type in firm_documents_columns_to_add.items():
        try:
            cursor.execute(f"ALTER TABLE firm_documents ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise

def upsert_firm_document(data):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check if a record already exists
    cursor.execute("SELECT id FROM firm_documents WHERE work_id = ? AND firm_name = ?", (data['work_id'], data['firm_name']))
    existing_id = cursor.fetchone()

    if existing_id:
        # UPDATE existing record
        query = """
            UPDATE firm_documents SET
                pg_type = ?, pg_no = ?, pg_amount = ?, pg_submitted_on = ?, pg_vetted_on = ?,
                bank_name = ?, bank_address = ?, firm_address = ?, indemnity_bond_details = ?,
                indemnity_submitted_on = ?, indemnity_vetted_on = ?, other_docs_details = ?,
                submission_date = ?, pg_submitted = ?, indemnity_bond_submitted = ?
            WHERE id = ?
        """
        params = (
            data.get('pg_type'), data.get('pg_no'), data.get('pg_amount'), data.get('pg_submitted_on'), data.get('pg_vetted_on'),
            data.get('bank_name'), data.get('bank_address'), data.get('firm_address'), data.get('indemnity_bond_details'),
            data.get('indemnity_submitted_on'), data.get('indemnity_vetted_on'), data.get('other_docs_details'),
            data.get('submission_date'), data.get('pg_submitted'), data.get('indemnity_bond_submitted'),
            existing_id[0]
        )
    else:
        # INSERT new record
        query = """
            INSERT INTO firm_documents (
                work_id, firm_name, pg_type, pg_no, pg_amount, pg_submitted_on, pg_vetted_on,
                bank_name, bank_address, firm_address, indemnity_bond_details,
                indemnity_submitted_on, indemnity_vetted_on, other_docs_details,
                submission_date, pg_submitted, indemnity_bond_submitted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data.get('work_id'), data.get('firm_name'), data.get('pg_type'), data.get('pg_no'), data.get('pg_amount'), data.get('pg_submitted_on'), data.get('pg_vetted_on'),
            data.get('bank_name'), data.get('bank_address'), data.get('firm_address'), data.get('indemnity_bond_details'),
            data.get('indemnity_submitted_on'), data.get('indemnity_vetted_on'), data.get('other_docs_details'),
            data.get('submission_date'), data.get('pg_submitted'), data.get('indemnity_bond_submitted')
        )
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_firm_documents(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, 
               firm_address, indemnity_bond_details, other_docs_details, submission_date, 
               pg_submitted, indemnity_bond_submitted, pg_type, pg_submitted_on, 
               pg_vetted_on, indemnity_submitted_on, indemnity_vetted_on 
        FROM firm_documents WHERE work_id = ?
    """, (work_id,))
    documents = cursor.fetchall()
    conn.close()
    return documents

def get_firm_document_by_work_and_firm_name(work_id, firm_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, 
               firm_address, indemnity_bond_details, other_docs_details, submission_date, 
               pg_submitted, indemnity_bond_submitted, pg_type, pg_submitted_on, 
               pg_vetted_on, indemnity_submitted_on, indemnity_vetted_on 
        FROM firm_documents WHERE work_id = ? AND firm_name = ?
    """, (work_id, firm_name))
    document = cursor.fetchone()
    conn.close()
    if document:
        return {
            'id': document[0],
            'work_id': document[1],
            'firm_name': document[2],
            'pg_no': document[3],
            'pg_amount': document[4],
            'bank_name': document[5],
            'bank_address': document[6],
            'firm_address': document[7],
            'indemnity_bond_details': document[8],
            'other_docs_details': document[9],
            'submission_date': document[10],
            'pg_submitted': document[11],
            'indemnity_bond_submitted': document[12],
            'pg_type': document[13],
            'pg_submitted_on': document[14],
            'pg_vetted_on': document[15],
            'indemnity_submitted_on': document[16],
            'indemnity_vetted_on': document[17]
        }
    return None

def delete_firm_document(doc_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firm_documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
