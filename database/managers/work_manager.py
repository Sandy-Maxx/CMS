import sqlite3
from config import DATABASE_PATH

def create_works_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    columns_to_add = {
        "justification": "TEXT",
        "section": "TEXT",
        "work_type": "TEXT",
        "file_no": "TEXT",
        "estimate_no": "TEXT",
        "tender_cost": "REAL",
        "tender_opening_date": "TEXT",
        "loa_no": "TEXT",
        "loa_date": "TEXT",
        "work_commence_date": "TEXT"
    }

    for column, col_type in columns_to_add.items():
        try:
            cursor.execute(f"ALTER TABLE works ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise

def add_work(name, description, justification=None, section=None, work_type=None, file_no=None, estimate_no=None, tender_cost=None, tender_opening_date=None, loa_no=None, loa_date=None, work_commence_date=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO works (name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date))
        work_id = cursor.lastrowid
        conn.commit()
        return work_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_work(work_id, name, description, justification=None, section=None, work_type=None, file_no=None, estimate_no=None, tender_cost=None, tender_opening_date=None, loa_no=None, loa_date=None, work_commence_date=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE works SET name = ?, description = ?, justification = ?, section = ?, work_type = ?, file_no = ?, estimate_no = ?, tender_cost = ?, tender_opening_date = ?, loa_no = ?, loa_date = ?, work_commence_date = ? WHERE id = ?", (name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date, work_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_work_by_id(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date FROM works WHERE id = ?", (work_id,))
    work = cursor.fetchone()
    conn.close()
    return {'work_id': work[0], 'work_name': work[1], 'description': work[2], 'justification': work[3], 'section': work[4], 'work_type': work[5], 'file_no': work[6], 'estimate_no': work[7], 'tender_cost': work[8], 'tender_opening_date': work[9], 'loa_no': work[10], 'loa_date': work[11], 'work_commence_date': work[12]} if work else None

def get_works():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date FROM works")
    works = cursor.fetchall()
    conn.close()
    return [(w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], w[10], w[11], w[12]) for w in works]

def get_works_by_name(search_term):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, justification, section, work_type, file_no, estimate_no, tender_cost, tender_opening_date, loa_no, loa_date, work_commence_date FROM works WHERE name LIKE ?", ('%' + search_term + '%',))
    works = cursor.fetchall()
    conn.close()
    return [(w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], w[10], w[11], w[12]) for w in works]

def delete_work(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM schedule_item_variations WHERE schedule_item_id IN (SELECT id FROM schedule_items WHERE work_id = ?)", (work_id,))
        cursor.execute("DELETE FROM firm_rates WHERE schedule_item_id IN (SELECT id FROM schedule_items WHERE work_id = ?)", (work_id,))
        cursor.execute("DELETE FROM schedule_items WHERE work_id = ?", (work_id,))
        cursor.execute("DELETE FROM works WHERE id = ?", (work_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error during delete_work: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
