import sqlite3
from . import Connection

def getMlfbByHwType(hw_type):
    cursor = Connection.getCursor()
    cursor.execute('SELECT mlfb FROM CPU_List WHERE type = ?', (hw_type,))
    return cursor.fetchall()