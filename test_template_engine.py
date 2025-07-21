import os
from database import db_manager
from features.template_engine.template_processor import TemplateProcessor
from features.template_engine.data_manager import TemplateDataManager

def test_template_engine():
    print("--- Testing Template Engine ---")

    # 1. Add a test work
    print("Step 1: Adding a test work...")
    work_id = db_manager.add_work(name="Template Engine Test Work", description="Test work for template engine.")
    if not work_id:
        print("FAILURE: Could not create work")
        return
    print(f"SUCCESS: Work added with ID: {work_id}")

    # 2. Setup template and data
    print("\nStep 2: Setting up template and data...")
    template_path = "test_template.docx"
    data_manager = TemplateDataManager()
    template_processor = TemplateProcessor()
    
    # 3. Save some initial data
    print("\nStep 3: Saving initial data...")
    initial_data = {"NAME": "Test User"}
    data_manager.save_template_data(template_path, initial_data)
    print("SUCCESS: Initial data saved.")

    # 4. Load the data
    print("\nStep 4: Loading data...")
    loaded_data = data_manager.load_template_data(template_path)
    # Extract the 'current' value for the 'NAME' placeholder
    name_value = loaded_data.get("NAME", {}).get("current")
    if name_value == "Test User":
        print(f"SUCCESS: Loaded data: {loaded_data}")
    else:
        print(f"FAILURE: Loaded data is incorrect: {loaded_data}")

    # 5. Process the template
    print("\nStep 5: Processing the template...")
    output_path = "test_output.docx"
    # The `replace_placeholders` method expects a dictionary of placeholder values.
    # We'll pass the `initial_data` directly.
    success, message = template_processor.replace_placeholders(template_path, initial_data, work_id, output_path, firm_placeholders=set())

    if success:
        print(f"SUCCESS: {message}")
        if os.path.exists(output_path):
            print(f"SUCCESS: Output file created at: {output_path}")
            # TODO: Add verification of the content of the output file
            os.remove(output_path)
        else:
            print("FAILURE: Output file not created.")
    else:
        print(f"FAILURE: {message}")

    # 6. Clean up the database and dummy files
    print("\nStep 6: Cleaning up...")
    db_manager.delete_work(work_id)
    os.remove(template_path)
    # Clean up the generated json file
    data_file = data_manager._get_template_data_path(template_path)
    if os.path.exists(data_file):
        os.remove(data_file)
    print("SUCCESS: Test work and dummy files deleted.")

if __name__ == "__main__":
    db_manager.create_tables()
    test_template_engine()
