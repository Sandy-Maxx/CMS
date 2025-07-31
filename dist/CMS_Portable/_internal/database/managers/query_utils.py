import sqlite3
from config import DATABASE_PATH

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
