import sqlite3
from . import Connection

def saveDll(Tia_Version, dll_Path):
    cursor = Connection.getCursor()
    try:
        cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (Tia_Version, dll_Path))
        cursor.connection.commit()
        print("DLL path saved successfully.")
        return True
    except sqlite3.IntegrityError:
        print("Error: A DLL path for TIA version {} already exists in the database.".format(Tia_Version))
        return False
    except sqlite3.Error as e:
        print("An error occurred while executing the SQL query:", e)
        return False
    except Exception as e:
        print("An unexpected error occurred:", e)
        return False
        
        
def getDllPath(Tia_Version):
    try:

        cursor = Connection.getCursor()
        cursor.execute('SELECT path FROM Dll_Path WHERE Tia_Version = ?', (Tia_Version,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except sqlite3.Error as e:
        print("An error occurred while executing the SQL query:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None
        

def CheckDll(Tia_Version):
    if getDllPath(Tia_Version):
        return True
    else:
        return False