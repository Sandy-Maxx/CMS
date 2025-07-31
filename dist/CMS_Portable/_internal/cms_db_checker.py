import sqlite3
from config import DATABASE_PATH

def check_works_table_empty():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM works")
    count = cursor.fetchone()[0]
    conn.close()
    if count == 0:
        print("The 'works' table is empty.")
        return True
    else:
        print(f"The 'works' table contains {count} entries.")
        return False

if __name__ == "__main__":
    check_works_table_empty()