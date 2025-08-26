# src/dosint/core/database.py (Improved Version)

from tinydb import TinyDB, Query
import os

DB_PATH = 'data/main_db.json'

def _get_db():
    """Helper function to ensure the data directory exists and return a DB connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return TinyDB(DB_PATH)

def add_report(indicators):
    """Adds a report with multiple indicators."""
    db = _get_db()
    db.insert(indicators)
    db.close() # Close the connection after the operation
    return True

def find_reports(key, value):
    """Finds all reports containing a specific key-value pair."""
    db = _get_db()
    results = db.search(Query()[key] == value)
    db.close() # Close the connection after the operation
    return results
