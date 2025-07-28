import sqlite3
from config import DATABASE_PATH

def create_schedule_item_variations_table(cursor):
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

def add_schedule_item_variation(schedule_item_id, variation_name, quantity):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO schedule_item_variations (schedule_item_id, variation_name, quantity) VALUES (?, ?, ?)",
            (schedule_item_id, str(variation_name), quantity)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # If it already exists, update it instead of failing
        cursor.execute(
            "UPDATE schedule_item_variations SET quantity = ? WHERE schedule_item_id = ? AND variation_name = ?",
            (quantity, schedule_item_id, str(variation_name))
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def update_schedule_item_variation(schedule_item_id, variation_name, quantity):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule_item_variations SET quantity = ? WHERE schedule_item_id = ? AND variation_name = ?",
        (quantity, schedule_item_id, str(variation_name))
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
