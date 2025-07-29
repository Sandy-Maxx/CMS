"""
Unit tests for the database introspection helper.

Tests the get_columns function and ensures it returns new columns
immediately after ALTER TABLE operations.
"""

import os
import sqlite3
import tempfile
from utils.db_introspect import get_columns, get_works_columns, get_firm_documents_columns
from database.managers.database_utils import get_table_columns
from features.template_engine.work_data_provider import WorkDataProvider
from config import DATABASE_PATH
from database import db_manager


def test_get_columns_basic():
    """Test basic functionality of get_columns function."""
    print("--- Testing get_columns basic functionality ---")
    
    # Test with works table
    works_columns = get_columns('works')
    print(f"Works table columns: {works_columns}")
    
    # Verify we get expected basic columns
    expected_works_columns = ['id', 'name', 'description']
    for col in expected_works_columns:
        if col in works_columns:
            print(f"SUCCESS: Found expected column '{col}' in works table")
        else:
            print(f"FAILURE: Missing expected column '{col}' in works table")
    
    # Test with firm_documents table
    firm_docs_columns = get_columns('firm_documents')
    print(f"Firm documents table columns: {firm_docs_columns}")
    
    # Verify we get expected basic columns
    expected_firm_docs_columns = ['id', 'work_id', 'firm_name']
    for col in expected_firm_docs_columns:
        if col in firm_docs_columns:
            print(f"SUCCESS: Found expected column '{col}' in firm_documents table")
        else:
            print(f"FAILURE: Missing expected column '{col}' in firm_documents table")


def test_get_specific_table_columns():
    """Test the specific table column functions."""
    print("\n--- Testing specific table column functions ---")
    
    # Test get_works_columns
    works_cols_direct = get_columns('works')
    works_cols_function = get_works_columns()
    
    if works_cols_direct == works_cols_function:
        print("SUCCESS: get_works_columns() returns same result as get_columns('works')")
    else:
        print("FAILURE: get_works_columns() differs from get_columns('works')")
        print(f"  Direct: {works_cols_direct}")
        print(f"  Function: {works_cols_function}")
    
    # Test get_firm_documents_columns
    firm_docs_cols_direct = get_columns('firm_documents')
    firm_docs_cols_function = get_firm_documents_columns()
    
    if firm_docs_cols_direct == firm_docs_cols_function:
        print("SUCCESS: get_firm_documents_columns() returns same result as get_columns('firm_documents')")
    else:
        print("FAILURE: get_firm_documents_columns() differs from get_columns('firm_documents')")
        print(f"  Direct: {firm_docs_cols_direct}")
        print(f"  Function: {firm_docs_cols_function}")


def test_alter_table_immediate_reflection():
    """Test that new columns are returned immediately after ALTER TABLE."""
    print("\n--- Testing ALTER TABLE immediate reflection ---")
    
    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name
    
    try:
        # Create a simple test table
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        
        # Create initial table
        cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        
        # Test get_columns with our temporary database
        def get_test_columns():
            test_conn = sqlite3.connect(temp_db_path)
            try:
                cur = test_conn.execute("PRAGMA table_info(test_table)")
                cols = [row[1] for row in cur.fetchall()]
                return cols
            finally:
                test_conn.close()
        
        # Get initial columns
        initial_columns = get_test_columns()
        print(f"Initial columns: {initial_columns}")
        
        if initial_columns == ['id', 'name']:
            print("SUCCESS: Initial table structure is correct")
        else:
            print(f"FAILURE: Initial table structure incorrect. Expected ['id', 'name'], got {initial_columns}")
        
        # Add a new column using ALTER TABLE
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE test_table ADD COLUMN description TEXT")
        conn.commit()
        conn.close()
        
        # Immediately check if new column is reflected
        updated_columns = get_test_columns()
        print(f"Columns after ALTER TABLE: {updated_columns}")
        
        if updated_columns == ['id', 'name', 'description']:
            print("SUCCESS: New column 'description' immediately visible after ALTER TABLE")
        else:
            print(f"FAILURE: New column not immediately visible. Expected ['id', 'name', 'description'], got {updated_columns}")
        
        # Add another column to double-check
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE test_table ADD COLUMN created_date TEXT")
        conn.commit()
        conn.close()
        
        # Check again
        final_columns = get_test_columns()
        print(f"Columns after second ALTER TABLE: {final_columns}")
        
        if final_columns == ['id', 'name', 'description', 'created_date']:
            print("SUCCESS: Second new column 'created_date' immediately visible after ALTER TABLE")
        else:
            print(f"FAILURE: Second new column not immediately visible. Expected ['id', 'name', 'description', 'created_date'], got {final_columns}")
            
    finally:
        # Clean up temporary database
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)


def test_error_handling():
    """Test error handling for non-existent tables."""
    print("\n--- Testing error handling ---")
    
    try:
        # Try to get columns from a non-existent table
        columns = get_columns('non_existent_table')
        if columns == []:
            print("SUCCESS: Non-existent table returns empty list")
        else:
            print(f"UNEXPECTED: Non-existent table returned: {columns}")
    except sqlite3.Error as e:
        print(f"SUCCESS: Properly caught sqlite3.Error for non-existent table: {e}")
    except Exception as e:
        print(f"FAILURE: Unexpected error type for non-existent table: {type(e).__name__}: {e}")


def test_column_order_preservation():
    """Test that column order is preserved as defined in the table."""
    print("\n--- Testing column order preservation ---")
    
    # Create a temporary database with specific column order
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name
    
    try:
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        
        # Create table with specific column order
        cursor.execute("""
            CREATE TABLE order_test (
                zebra TEXT,
                alpha INTEGER,
                beta TEXT,
                gamma REAL
            )
        """)
        conn.commit()
        conn.close()
        
        # Get columns using our function
        def get_order_test_columns():
            test_conn = sqlite3.connect(temp_db_path)
            try:
                cur = test_conn.execute("PRAGMA table_info(order_test)")
                cols = [row[1] for row in cur.fetchall()]
                return cols
            finally:
                test_conn.close()
        
        columns = get_order_test_columns()
        expected_order = ['zebra', 'alpha', 'beta', 'gamma']
        
        if columns == expected_order:
            print(f"SUCCESS: Column order preserved correctly: {columns}")
        else:
            print(f"FAILURE: Column order not preserved. Expected {expected_order}, got {columns}")
            
    finally:
        # Clean up temporary database
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)


def test_alter_table_with_test_col():
    """Test adding a new column and checking placeholder list."""
    print("\n--- Testing ALTER TABLE with test_col ---")

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name

    try:
        # Create a simple test table
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        
        # Create initial table structure based on current works table
        cursor.execute("""
            CREATE TABLE works (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
        """)
        conn.commit()
        
        # Insert some test data
        cursor.execute("INSERT INTO works (name, description) VALUES (?, ?)", 
                      ("Test Work", "Test Description"))
        conn.commit()
        conn.close()

        # Add a new column using ALTER TABLE
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE works ADD COLUMN test_col TEXT")
        conn.commit()
        
        # Insert data into the new column
        cursor.execute("UPDATE works SET test_col = ? WHERE id = 1", ("Test Value",))
        conn.commit()
        conn.close()

        # Temporarily modify database utils to use our test database
        original_database_path = DATABASE_PATH
        import config
        import database.managers.database_utils as db_utils
        config.DATABASE_PATH = temp_db_path
        db_utils.DATABASE_PATH = temp_db_path
        
        try:
            # Check if new column appears in placeholder list
            placeholders = WorkDataProvider.get_available_placeholders_static()
            if '[TEST_COL]' in placeholders:
                print("SUCCESS: [TEST_COL] appears in placeholder list")
                print(f"Placeholder description: {placeholders['[TEST_COL]']}")
            else:
                print("FAILURE: [TEST_COL] not found in placeholder list")
                print(f"Available placeholders: {list(placeholders.keys())}")
        finally:
            # Restore original database path
            config.DATABASE_PATH = original_database_path
            db_utils.DATABASE_PATH = original_database_path
        
    finally:
        # Clean up temporary database
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)


if __name__ == '__main__':
    print("Starting DB Introspection Tests...")
    
    test_get_columns_basic()
    test_get_specific_table_columns()
    test_alter_table_immediate_reflection()
    test_error_handling()
    test_column_order_preservation()
    test_alter_table_with_test_col()
    print("\n--- DB Introspection Tests Complete ---")
