import sqlite3
from . import Connection

def saveDll(Tia_Version, dll_Path):
    cursor = Connection.getCursor()
    try:
        cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
        cursor.connection.commit()
    except:
        print("An exception occurred")
        
def getDllPath(Tia_Version):
    cursor = Connection.getCursor()
    try:
        cursor.execute('SELECT path FROM Dll_Path WHERE Tia_Version = ?', (Tia_Version,))
        return cursor.fetchone()
    except:
        print("An exception occurred")