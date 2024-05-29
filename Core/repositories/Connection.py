import sqlite3
from . import ValidateDb

instance = None
cursor = None

def setInstance():
    global cursor
    ValidateDb.validate_db()
    conn = sqlite3.connect("Openness.db")
    cursor = conn.cursor()

def getCursor():
    global instance, cursor
    if not instance or not cursor:
        print("Setting cursor instance")
        setInstance()
    return cursor
