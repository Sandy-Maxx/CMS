import sqlite3
from config import DATABASE_PATH
from datetime import datetime

def create_template_data_table(cursor):
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

def upsert_template_data(template_name, placeholder_name, value):
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
