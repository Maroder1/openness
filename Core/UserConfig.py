import sqlite3
import os
    
# current_path = os.path.dirname(os.path.abspath(__file__))
# conn_path = os.path.join(current_path, "Openness.db")

conn = sqlite3.connect("Openness.db")
cursor = conn.cursor()

def saveDll(self, Tia_Version, dll_Path):
    cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
    conn.commit()
    conn.close()