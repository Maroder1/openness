import sqlite3
import os
from . import ValidateDb

current_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_path, "Openness.db")

def getCursor():
    ValidateDb.validate_db()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor
