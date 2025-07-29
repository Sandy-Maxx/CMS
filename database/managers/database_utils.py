import sqlite3
import shutil
import os
from config import DATABASE_PATH

def backup_database(destination_path):
    try:
        shutil.copy2(DATABASE_PATH, destination_path)
        return True, f"Database backed up successfully to {destination_path}"
    except Exception as e:
        return False, f"Error backing up database: {e}"

def restore_database(source_path):
    try:
        # Close any existing connections to the database before restoring
        # This is crucial to avoid database locking issues on Windows
        # For simplicity, we'll assume the main application handles closing its connection
        # before calling this function, or that the application is restarted after restore.
        shutil.copy2(source_path, DATABASE_PATH)
        return True, f"Database restored successfully from {source_path}"
    except Exception as e:
        return False, f"Error restoring database: {e}"

def get_table_columns(table_name):
    """Get list of column names for a specific table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        # Return list of column names (index 1 in the PRAGMA result)
        return [col[1] for col in columns]
    finally:
        conn.close()

def get_work_columns():
    """Get list of column names for the works table."""
    return get_table_columns('works')

def get_firm_documents_columns():
    """Get list of column names for the firm_documents table."""
    return get_table_columns('firm_documents')
