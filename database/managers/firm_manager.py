import sqlite3
from config import DATABASE_PATH

def create_firms_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            representative TEXT,
            address TEXT
        )
    """)

def add_firm(name, representative, address):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO firms (name, representative, address) VALUES (?, ?, ?)", (name, representative, address))
        firm_id = cursor.lastrowid
        conn.commit()
        return firm_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_all_registered_firm_names():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM firms")
    firms = cursor.fetchall()
    conn.close()
    return [f[0] for f in firms]
