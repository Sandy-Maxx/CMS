from database.db_manager import create_tables, add_work, add_schedule_item, upsert_firm_rate
from datetime import datetime
import sqlite3

def populate_sample_data():
    create_tables()
    
    # Check if work already exists
    conn = sqlite3.connect('D:\\CMS\\CMS\\cms_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM works WHERE name = ?", ("Sample Project",))
    existing_work = cursor.fetchone()
    conn.close()
    
    if existing_work:
        work_id = existing_work[0]
        print(f"Work 'Sample Project' already exists with ID {work_id}.")
    else:
        work_id = add_work("Sample Project", "A test construction project")
        if not work_id:
            print("Failed to add work. It may already exist.")
            return
    
    # Add sample schedule items
    item1_id = add_schedule_item(work_id, "Concrete Pouring", "m³", 100.0, None)
    item2_id = add_schedule_item(work_id, "Steel Reinforcement", "kg", 500.0, None)
    item3_id = add_schedule_item(work_id, "Sub-item: Rebar Cutting", "kg", 200.0, item2_id)
    
    # Add sample firm rates
    upsert_firm_rate(item1_id, "Firm A", 50.0)
    upsert_firm_rate(item1_id, "Firm B", 55.0)
    upsert_firm_rate(item2_id, "Firm A", 2.0)
    upsert_firm_rate(item3_id, "Firm A", 1.5)

if __name__ == "__main__":
    populate_sample_data()