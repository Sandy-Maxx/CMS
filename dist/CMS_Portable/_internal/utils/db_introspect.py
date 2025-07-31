"""
Database introspection utilities for CMS application.

This module provides functions to introspect database table schemas,
particularly for getting column information from SQLite tables.
"""

import sqlite3
from config import DATABASE_PATH


def get_columns(table_name):
    """
    Returns ordered list of column names for the specified table.
    
    Args:
        table_name (str): Name of the database table to introspect
        
    Returns:
        list: Ordered list of column names as strings
        
    Raises:
        sqlite3.Error: If there's an error accessing the database
    """
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.execute(f"PRAGMA table_info({table_name})")
        cols = [row[1] for row in cur.fetchall()]
        return cols
    finally:
        conn.close()


def get_works_columns():
    """
    Returns ordered list of column names for the 'works' table.
    
    Returns:
        list: Ordered list of column names from the works table
    """
    return get_columns('works')


def get_firm_documents_columns():
    """
    Returns ordered list of column names for the 'firm_documents' table.
    
    Returns:
        list: Ordered list of column names from the firm_documents table
    """
    return get_columns('firm_documents')
