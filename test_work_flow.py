import sqlite3
from database import db_manager

def test_work_crud():
    print("--- Testing Work CRUD ---")
    
    # 1. Add a new work
    print("Step 1: Adding a new work...")
    work_id = db_manager.add_work(
        name="Test Work",
        description="This is a test work.",
        justification="Test Justification",
        section="Test Section",
        work_type="Test Type",
        file_no="Test File No",
        estimate_no="Test Estimate No",
        tender_cost=100000.0,
        tender_opening_date="2025-07-21",
        loa_no="Test LOA No",
        loa_date="2025-07-22",
        work_commence_date="2025-07-23"
    )
    if work_id:
        print(f"SUCCESS: Work added with ID: {work_id}")
    else:
        print("FAILURE: Failed to add work.")
        return

    # 2. Retrieve the work
    print("\nStep 2: Retrieving the work...")
    work = db_manager.get_work_by_id(work_id)
    if work and work['work_name'] == "Test Work":
        print(f"SUCCESS: Retrieved work: {work}")
    else:
        print("FAILURE: Failed to retrieve work.")
        return

    # 3. Update the work
    print("\nStep 3: Updating the work...")
    success = db_manager.update_work(
        work_id=work_id,
        name="Updated Test Work",
        description="This is an updated test work.",
        justification="Updated Justification",
        section="Updated Section",
        work_type="Updated Type",
        file_no="Updated File No",
        estimate_no="Updated Estimate No",
        tender_cost=200000.0,
        tender_opening_date="2025-08-01",
        loa_no="Updated LOA No",
        loa_date="2025-08-02",
        work_commence_date="2025-08-03"
    )
    if success:
        print("SUCCESS: Work updated.")
        updated_work = db_manager.get_work_by_id(work_id)
        if updated_work and updated_work['work_name'] == "Updated Test Work":
            print(f"SUCCESS: Verified updated work: {updated_work}")
        else:
            print("FAILURE: Failed to verify updated work.")
    else:
        print("FAILURE: Failed to update work.")
        return

    # 4. Delete the work
    print("\nStep 4: Deleting the work...")
    success = db_manager.delete_work(work_id)
    if success:
        print("SUCCESS: Work deleted.")
        deleted_work = db_manager.get_work_by_id(work_id)
        if not deleted_work:
            print("SUCCESS: Verified work deletion.")
        else:
            print("FAILURE: Failed to verify work deletion.")
    else:
        print("FAILURE: Failed to delete work.")

if __name__ == "__main__":
    db_manager.create_tables()
    test_work_crud()
