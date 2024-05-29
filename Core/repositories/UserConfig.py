import sqlite3
from . import Connection

def saveDll(Tia_Version, dll_Path):
    cursor = Connection.getCursor()
    cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
    cursor.connection.commit()