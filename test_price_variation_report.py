import os
from database import db_manager
from features.price_variation.price_variation_exporter import export_price_variation_data_to_excel

def test_price_variation_report():
    print("--- Testing Price Variation Report ---")

    # 1. Add a test work
    print("Step 1: Adding a test work...")
    work_id = db_manager.add_work(name="Price Variation Test Work", description="Test work for price variation report.")
    if not work_id:
        print("FAILURE: Could not create work")
        return
    print(f"SUCCESS: Work added with ID: {work_id}")

    # 2. Add schedule items
    print("\nStep 2: Adding schedule items...")
    item1_id = db_manager.add_schedule_item(work_id, "Item 1", "m3", 100)
    item2_id = db_manager.add_schedule_item(work_id, "Item 2", "nos", 20)
    print(f"SUCCESS: Added schedule items with IDs: {item1_id}, {item2_id}")

    # 3. Add firm rates
    print("\nStep 3: Adding firm rates...")
    db_manager.upsert_firm_rate(item1_id, "Firm A", 1500)
    db_manager.upsert_firm_rate(item2_id, "Firm A", 500)
    print("SUCCESS: Added firm rates for Firm A.")

    # 4. Add variations
    print("\nStep 4: Adding variations...")
    db_manager.add_schedule_item_variation(item1_id, "Price Var 1", 130) # > 125%
    db_manager.add_schedule_item_variation(item2_id, "Price Var 1", 30) # > 140%
    print("SUCCESS: Added variations.")

    # 5. Prepare data for export
    print("\nStep 5: Preparing data for export...")
    work_details = db_manager.get_work_by_id(work_id)
    schedule_items = db_manager.get_schedule_items(work_id)
    selected_firms = ["Firm A"]
    variation_name = "Price Var 1"

    print("SUCCESS: Data prepared for export.")

    # 6. Export the report
    print("\nStep 6: Exporting the report...")
    output_path = os.path.join(os.getcwd(), "test_price_variation_report.xlsx")
    success, message = export_price_variation_data_to_excel(
        work_details,
        schedule_items,
        output_path,
        selected_firms,
        variation_name
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
    test_price_variation_report()
