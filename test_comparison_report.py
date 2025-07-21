import os
from database import db_manager
from features.comparison.comparison_exporter import ComparisonExporter

def test_comparison_report():
    print("--- Testing Comparison Report ---")

    # 1. Add a test work
    print("Step 1: Adding a test work...")
    work_id = db_manager.add_work(name="Comparison Test Work", description="Test work for comparison report.")
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

    # 4. Export the report
    print("\nStep 4: Exporting the report...")
    output_path = os.path.join(os.getcwd(), "test_comparison_report.xlsx")
    try:
        exporter = ComparisonExporter(work_id)
        exporter.export_to_excel(output_path)
        print(f"SUCCESS: Report exported to {output_path}")
        if os.path.exists(output_path):
            print(f"SUCCESS: Report file created at: {output_path}")
            os.remove(output_path)
        else:
            print("FAILURE: Report file not created.")
    except Exception as e:
        print(f"FAILURE: {e}")
        import traceback
        traceback.print_exc()


    # 5. Clean up the database
    print("\nStep 5: Cleaning up the database...")
    db_manager.delete_work(work_id)
    print("SUCCESS: Test work deleted.")

if __name__ == "__main__":
    db_manager.create_tables()
    test_comparison_report()

