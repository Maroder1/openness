import sqlite3
from . import Connection

def saveDll(self, Tia_Version, dll_Path):
    Connection.getCursor
    cursor = Connection.getCursor()
    cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
    cursor.commit()