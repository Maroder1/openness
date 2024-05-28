import sqlite3
import os
class UserConfig:
    
    conn_path = ""
    
    def __init__(self, conn_path):
        self.conn_path = conn_path
    

    conn = sqlite3.connect(conn_path)
    cursor = conn.cursor()

    def saveDll(self, Tia_Version, dll_Path):
        self.cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
        self.conn.commit()
        self.conn.close()