import sqlite3
from config import DATABASE_PATH

def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    # Add new columns if they don't exist
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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_id INTEGER,
            parent_item_id INTEGER,
            item_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            FOREIGN KEY (work_id) REFERENCES works(id),
            FOREIGN KEY (parent_item_id) REFERENCES schedule_items(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firm_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_item_id INTEGER,
            firm_name TEXT NOT NULL,
            unit_rate REAL NOT NULL,
            date_recorded TEXT NOT NULL,
            FOREIGN KEY (schedule_item_id) REFERENCES schedule_items(id),
            UNIQUE(schedule_item_id, firm_name)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS template_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT NOT NULL,
            placeholder_name TEXT NOT NULL,
            value TEXT,
            timestamp TEXT NOT NULL,
            UNIQUE(template_name, placeholder_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule_item_variations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_item_id INTEGER,
            variation_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            FOREIGN KEY (schedule_item_id) REFERENCES schedule_items(id),
            UNIQUE(schedule_item_id, variation_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            representative TEXT,
            address TEXT
        )
    """)
    
    conn.commit()
    conn.close()

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

def add_schedule_item(work_id, item_name, unit, quantity, parent_item_id=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schedule_items (work_id, parent_item_id, item_name, quantity, unit) VALUES (?, ?, ?, ?, ?)",
        (work_id, parent_item_id, item_name, quantity, unit)
    )
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def update_schedule_item(item_id, item_name, unit, quantity, parent_item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule_items SET item_name = ?, unit = ?, quantity = ?, parent_item_id = ? WHERE id = ?",
        (item_name, unit, quantity, parent_item_id, item_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_schedule_items(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, parent_item_id, item_name, quantity, unit FROM schedule_items WHERE work_id = ?", (work_id,))
    items = cursor.fetchall()
    conn.close()
    return [{'item_id': i[0], 'parent_item_id': i[1], 'item_name': i[2], 'quantity': i[3], 'unit': i[4]} for i in items]

def get_schedule_item_by_id(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, parent_item_id, item_name, quantity, unit FROM schedule_items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return {'item_id': item[0], 'parent_item_id': item[1], 'item_name': item[2], 'quantity': item[3], 'unit': item[4]} if item else None

def delete_schedule_item(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedule_item_variations WHERE schedule_item_id = ?", (item_id,))
    cursor.execute("DELETE FROM firm_rates WHERE schedule_item_id = ?", (item_id,))
    cursor.execute("DELETE FROM schedule_items WHERE parent_item_id = ?", (item_id,))
    cursor.execute("DELETE FROM schedule_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def upsert_firm_rate(schedule_item_id, firm_name, unit_rate):
    from datetime import datetime
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    date_recorded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO firm_rates (schedule_item_id, firm_name, unit_rate, date_recorded) VALUES (?, ?, ?, ?)",
            (schedule_item_id, firm_name, unit_rate, date_recorded)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        cursor.execute(
            "UPDATE firm_rates SET unit_rate = ?, date_recorded = ? WHERE schedule_item_id = ? AND firm_name = ?",
            (unit_rate, date_recorded, schedule_item_id, firm_name)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_firm_rates(schedule_item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, firm_name, unit_rate, date_recorded FROM firm_rates WHERE schedule_item_id = ?",
        (schedule_item_id,)
    )
    rates = cursor.fetchall()
    conn.close()
    return [{'rate_id': r[0], 'firm_name': r[1], 'unit_rate': r[2], 'date_recorded': r[3]} for r in rates]

def get_firm_rate_by_id(rate_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, schedule_item_id, firm_name, unit_rate, date_recorded FROM firm_rates WHERE id = ?",
        (rate_id,)
    )
    rate = cursor.fetchone()
    conn.close()
    return {'rate_id': rate[0], 'schedule_item_id': rate[1], 'firm_name': rate[2], 'unit_rate': rate[3], 'date_recorded': rate[4]} if rate else None

def update_firm_rate(rate_id, firm_name, unit_rate):
    from datetime import datetime
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    date_recorded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE firm_rates SET unit_rate = ?, date_recorded = ? WHERE id = ?",
        (unit_rate, date_recorded, rate_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_firm_rate(rate_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firm_rates WHERE id = ?", (rate_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_firm_rate_by_item_and_firm(schedule_item_id, firm_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firm_rates WHERE schedule_item_id = ? AND firm_name = ?", (schedule_item_id, firm_name))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_all_unique_firm_names():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT firm_name FROM firm_rates")
    firms = cursor.fetchall()
    conn.close()
    return [f[0] for f in firms]

def get_unique_firm_names_by_work_id(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT fr.firm_name
        FROM firm_rates fr
        JOIN schedule_items si ON fr.schedule_item_id = si.id
        WHERE si.work_id = ?
    """, (work_id,))
    firms = cursor.fetchall()
    conn.close()
    return [f[0] for f in firms]

def get_all_unique_units():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT unit FROM schedule_items")
    units = cursor.fetchall()
    conn.close()
    return [u[0] for u in units]

def get_all_unique_sections():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT section FROM works WHERE section IS NOT NULL AND section != ''")
    sections = cursor.fetchall()
    conn.close()
    return [s[0] for s in sections]

def get_all_unique_file_numbers():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT file_no FROM works WHERE file_no IS NOT NULL AND file_no != ''")
    file_numbers = cursor.fetchall()
    conn.close()
    return [fn[0] for fn in file_numbers]

def get_all_unique_estimate_numbers():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT estimate_no FROM works WHERE estimate_no IS NOT NULL AND estimate_no != ''")
    estimate_numbers = cursor.fetchall()
    conn.close()
    return [en[0] for en in estimate_numbers]

def get_all_unique_loa_numbers():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT loa_no FROM works WHERE loa_no IS NOT NULL AND loa_no != ''")
    loa_numbers = cursor.fetchall()
    conn.close()
    return [ln[0] for ln in loa_numbers]


def upsert_template_data(template_name, placeholder_name, value):
    from datetime import datetime
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO template_data (template_name, placeholder_name, value, timestamp) VALUES (?, ?, ?, ?)",
            (template_name, placeholder_name, value, timestamp)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        cursor.execute(
            "UPDATE template_data SET value = ?, timestamp = ? WHERE template_name = ? AND placeholder_name = ?",
            (value, timestamp, template_name, placeholder_name)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_template_data(template_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT placeholder_name, value FROM template_data WHERE template_name = ?", (template_name,))
    data = cursor.fetchall()
    conn.close()
    return {d[0]: d[1] for d in data}

def add_schedule_item_variation(schedule_item_id, variation_name, quantity):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO schedule_item_variations (schedule_item_id, variation_name, quantity) VALUES (?, ?, ?)",
            (schedule_item_id, variation_name, quantity)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_schedule_item_variation(schedule_item_id, variation_name, quantity):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule_item_variations SET quantity = ? WHERE schedule_item_id = ? AND variation_name = ?",
        (quantity, schedule_item_id, variation_name)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_schedule_item_variations(schedule_item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT variation_name, quantity FROM schedule_item_variations WHERE schedule_item_id = ?",
        (schedule_item_id,)
    )
    variations = cursor.fetchall()
    conn.close()
    return {v[0]: v[1] for v in variations}

def delete_variation_by_name(work_id, variation_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM schedule_item_variations
            WHERE variation_name = ? AND schedule_item_id IN (
                SELECT id FROM schedule_items WHERE work_id = ?
            )
        """, (variation_name, work_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error during delete_variation_by_name: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_variation_names_for_work(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT siv.variation_name
        FROM schedule_item_variations siv
        JOIN schedule_items si ON siv.schedule_item_id = si.id
        WHERE si.work_id = ?
    """, (work_id,))
    variation_names = cursor.fetchall()
    conn.close()
    return [v[0] for v in variation_names]

def get_firm_documents(work_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted FROM firm_documents WHERE work_id = ?", (work_id,))
    documents = cursor.fetchall()
    conn.close()
    return documents

def get_firm_document_by_work_and_firm_name(work_id, firm_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, firm_address, indemnity_bond_details, other_docs_details, submission_date, pg_submitted, indemnity_bond_submitted FROM firm_documents WHERE work_id = ? AND firm_name = ?", (work_id, firm_name))
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
            'indemnity_bond_submitted': document[12]
        }
    return None