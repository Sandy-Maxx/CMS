import sqlite3
from config import DATABASE_PATH

def create_schedule_items_table(cursor):
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
