from tinydb import TinyDB, Query
import os

if not os.path.exists('data'): os.makedirs('data')
db = TinyDB('data/main_db.json')
ReportQuery = Query()

def add_report(indicators):
    db.insert(indicators)
    return True

def find_reports(key, value):
    return db.search(ReportQuery[key] == value)
