import sqlite3
from config import DATABASE_PATH
from datetime import datetime

def create_firm_rates_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firm_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_item_id INTEGER,
            firm_name TEXT NOT NULL,
            unit_rate REAL NOT NULL,
            labour_rate REAL,
            date_recorded TEXT NOT NULL,
            FOREIGN KEY (schedule_item_id) REFERENCES schedule_items(id),
            UNIQUE(schedule_item_id, firm_name)
        )
    """)

def upsert_firm_rate(schedule_item_id, firm_name, unit_rate, labour_rate=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    date_recorded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO firm_rates (schedule_item_id, firm_name, unit_rate, labour_rate, date_recorded) VALUES (?, ?, ?, ?, ?)",
            (schedule_item_id, firm_name, unit_rate, labour_rate, date_recorded)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        cursor.execute(
            "UPDATE firm_rates SET unit_rate = ?, labour_rate = ?, date_recorded = ? WHERE schedule_item_id = ? AND firm_name = ?",
            (unit_rate, labour_rate, date_recorded, schedule_item_id, firm_name)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_firm_rates(schedule_item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, firm_name, unit_rate, labour_rate, date_recorded FROM firm_rates WHERE schedule_item_id = ?",
        (schedule_item_id,)
    )
    rates = cursor.fetchall()
    conn.close()
    return [{'rate_id': r[0], 'firm_name': r[1], 'unit_rate': r[2], 'labour_rate': r[3], 'date_recorded': r[4]} for r in rates]

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

def get_firm_rate_for_item(schedule_item_id, firm_name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, schedule_item_id, firm_name, unit_rate, labour_rate, date_recorded FROM firm_rates WHERE schedule_item_id = ? AND firm_name = ?",
        (schedule_item_id, firm_name)
    )
    rate = cursor.fetchone()
    conn.close()
    if rate:
        return {'rate_id': rate[0], 'schedule_item_id': rate[1], 'firm_name': rate[2], 'rate': rate[3], 'labour_rate': rate[4], 'date_recorded': rate[5]}
    return None

def update_firm_rate(rate_id, firm_name, unit_rate):
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
