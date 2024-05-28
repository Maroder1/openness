import sqlite3
import os
    
current_path = os.path.dirname(os.path.abspath(__file__))
conn_path = os.path.join(current_path, "Openness.db")

conn = sqlite3.connect(conn_path)
cursor = conn.cursor()

def getMlfbByHwType(hw_type):
    cursor.execute('SELECT mlfb FROM CPU_List WHERE type = ?', (hw_type,))
    return cursor.fetchall()