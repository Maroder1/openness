import sqlite3
import os

current_path = os.path.abspath(__file__)
conn_path = os.path.join(os.path.dirname(current_path), "Database", "Openness.db")

conn = sqlite3.connect(conn_path)
cursor = conn.cursor()

def saveDll(self, Tia_Version, dll_Path):
    cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
    conn.commit()
    conn.close()