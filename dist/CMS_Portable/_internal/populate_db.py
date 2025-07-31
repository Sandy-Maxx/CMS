from database import db_manager
from database.db_manager import create_tables, add_work, add_schedule_item, upsert_firm_rate, delete_work, add_firm
from datetime import datetime
import sqlite3
import random

def populate_sample_data():
    create_tables()
    
    work_names = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta"]
    base_firms = ["Firm A", "Firm B", "Firm C", "Firm D"]

    for work_name in work_names:
        conn = sqlite3.connect('D:\\CMS\\CMS\\cms_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM works WHERE name = ?", (work_name,))
        existing_work = cursor.fetchone()
        conn.close()
        
        if existing_work:
            work_id = existing_work[0]
            print(f"Deleting existing work '{work_name}' with ID {work_id}...")
            delete_work(work_id)
            print(f"Existing work '{work_name}' deleted.")

        work_id = add_work(work_name, f"Description for {work_name}")
        if not work_id:
            print(f"Failed to add work {work_name}.")
            continue

        print(f"Populating data for {work_name} (ID: {work_id})...")

        # Generate unique firm names for this work
        work_firms = [f"{firm}-{work_name.split()[1]}" for firm in base_firms]

        # Register firms in the 'firms' table
        for firm in work_firms:
            db_manager.add_firm(firm, f"Representative for {firm}", f"Address for {firm}")

        # Add sample schedule items
        items_to_add = [
            ("Excavation", "m3", 100.0, None),
            ("Concrete Foundation", "m3", 50.0, None),
            ("Brickwork", "m2", 200.0, None),
            ("Roofing", "m2", 150.0, None),
            ("Plumbing Installation", "unit", 10.0, None),
            ("Electrical Wiring", "point", 120.0, None),
            ("Flooring (Tiles)", "m2", 80.0, None),
            ("Painting (Interior)", "m2", 300.0, None),
            ("HVAC System", "unit", 5.0, None),
            ("Landscaping", "m2", 500.0, None),
            ("Windows Installation", "unit", 20.0, None),
            ("Doors Installation", "unit", 15.0, None)
        ]

        added_item_ids = {}
        for item_name, unit, quantity, parent_name in items_to_add:
            parent_id = added_item_ids.get(parent_name) if parent_name else None
            item_id = add_schedule_item(work_id, item_name, unit, quantity, parent_id)
            if item_id:
                added_item_ids[item_name] = item_id

                # Add unique non-zero firm rates
                for firm in work_firms:
                    rate = round(random.uniform(5.0, 200.0), 2) # Generate unique non-zero rates
                    labour_rate = round(random.uniform(10.0, 50.0), 2) # Generate random labour rate
                    upsert_firm_rate(item_id, firm, rate, labour_rate)

        # Add sub-items and their rates
        sub_items_to_add = [
            ("Sub-item: Soil Removal", "m3", 50.0, "Excavation"),
            ("Sub-item: Rebar for Foundation", "kg", 1000.0, "Concrete Foundation"),
            ("Sub-item: Wall Plastering", "m2", 150.0, "Brickwork"),
            ("Sub-item: Water Heater Connection", "unit", 2.0, "Plumbing Installation")
        ]

        for item_name, unit, quantity, parent_name in sub_items_to_add:
            parent_id = added_item_ids.get(parent_name)
            if parent_id:
                item_id = add_schedule_item(work_id, item_name, unit, quantity, parent_id)
                if item_id:
                    added_item_ids[item_name] = item_id
                    for firm in work_firms:
                        rate = round(random.uniform(1.0, 100.0), 2) # Generate unique non-zero rates
                        labour_rate = round(random.uniform(5.0, 20.0), 2) # Generate random labour rate
                        upsert_firm_rate(item_id, firm, rate, labour_rate)

    print("All sample data populated successfully.")

if __name__ == "__main__":
    populate_sample_data()