import sqlite3
from . import ValidateDb

def getCursor():
    ValidateDb.validate_db()
    conn = sqlite3.connect("Openness.db")
    cursor = conn.cursor()
    return cursor
