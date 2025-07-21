import os
from database import db_manager
from features.vitiation.vitiation_data_exporter import export_vitiation_data_to_excel

def test_vitiation_report():
    print("--- Testing Vitiation Report ---")

    # 1. Add a test work
    print("Step 1: Adding a test work...")
    work_id = db_manager.add_work(name="Vitiation Test Work", description="Test work for vitiation report.")
    if not work_id:
        print("FAILURE: Could not create work")
        return
    print(f"SUCCESS: Work added with ID: {work_id}")

    # 2. Add schedule items
    print("\nStep 2: Adding schedule items...")
    item1_id = db_manager.add_schedule_item(work_id, "Item 1", "m3", 100)
    item2_id = db_manager.add_schedule_item(work_id, "Item 2", "nos", 20)
    print(f"SUCCESS: Added schedule items with IDs: {item1_id}, {item2_id}")

    # 3. Add firm rates for multiple firms
    print("\nStep 3: Adding firm rates...")
    db_manager.upsert_firm_rate(item1_id, "Firm A", 1500)
    db_manager.upsert_firm_rate(item2_id, "Firm A", 500)
    db_manager.upsert_firm_rate(item1_id, "Firm B", 1600)
    db_manager.upsert_firm_rate(item2_id, "Firm B", 450)
    print("SUCCESS: Added firm rates for Firm A and Firm B.")

    # 4. Add variations
    print("\nStep 4: Adding variations...")
    db_manager.add_schedule_item_variation(item1_id, "Vitiation 1", 120)
    db_manager.add_schedule_item_variation(item2_id, "Vitiation 1", 15)
    print("SUCCESS: Added variations.")

    # 5. Prepare data for export
    print("\nStep 5: Preparing data for export...")
    work_details = db_manager.get_work_by_id(work_id)
    all_items_from_db = db_manager.get_schedule_items(work_id)
    selected_firms = ["Firm A", "Firm B"]
    selected_variation_name = "Vitiation 1"

    processed_schedule_items = []
    item_map = {item['item_id']: dict(item) for item in all_items_from_db}
    for item_id, item_data in item_map.items():
        item_data['children'] = []
        item_data['firm_rates'] = db_manager.get_firm_rates(item_id)
        item_data['variations'] = db_manager.get_schedule_item_variations(item_id)
        item_data['level'] = 0
    for item_id, item_data in item_map.items():
        parent_id = item_data.get('parent_item_id')
        if parent_id is not None and parent_id in item_map:
            item_map[parent_id]['children'].append(item_data)
    root_items = [item for item in item_map.values() if item.get('parent_item_id') is None]
    root_items.sort(key=lambda x: x['item_name'])

    def flatten_and_process_recursive(items_list, parent_sr_prefix=""):
        sr_counter = 1
        for item in items_list:
            current_sr_no = f"{parent_sr_prefix}.{sr_counter}" if parent_sr_prefix else str(sr_counter)
            sr_counter += 1
            processed_item = item.copy()
            processed_item['sr_no'] = current_sr_no
            processed_schedule_items.append(processed_item)
            if item['children']:
                item['children'].sort(key=lambda x: x['item_name'])
                flatten_and_process_recursive(item['children'], current_sr_no)
    
    flatten_and_process_recursive(root_items)

    print("SUCCESS: Data prepared for export.")

    # 6. Export the report
    print("\nStep 6: Exporting the report...")
    output_path = os.path.join(os.getcwd(), "test_vitiation_report.xlsx")
    success, message = export_vitiation_data_to_excel(
        work_details,
        processed_schedule_items,
        output_path,
        selected_firms,
        selected_variation_name
    )

    if success:
        print(f"SUCCESS: {message}")
        if os.path.exists(output_path):
            print(f"SUCCESS: Report file created at: {output_path}")
            os.remove(output_path)
        else:
            print("FAILURE: Report file not created.")
    else:
        print(f"FAILURE: {message}")

    # 7. Clean up the database
    print("\nStep 7: Cleaning up the database...")
    db_manager.delete_work(work_id)
    print("SUCCESS: Test work deleted.")

if __name__ == "__main__":
    db_manager.create_tables()
    test_vitiation_report()
