import subprocess
import sqlite3
import csv
import os

current_path = os.path.abspath(__file__)
core_path = os.path.join(os.path.dirname(current_path), "Core")

db_path = os.path.join(core_path, "Openness.db")
requirements_path = os.path.join(core_path, "requirements")
ddl_path = os.path.join(core_path, "Database", "ddl.sql")
plc_List_path = os.path.join(core_path, "Database", "mlfb", "PLC_List.csv")

print(plc_List_path)

def install_dependencies():
    uninstall_dependencies()
    global requirements_path
    requirements_file = os.path.join(requirements_path, "requirements.txt")
    subprocess.call(["pip", "install", "-r", requirements_file])
    
def uninstall_dependencies():
    global requirements_path
    requirements_file = os.path.join(requirements_path, "uninstall.txt")
    subprocess.call(["pip", "uninstall", "-r", requirements_file])

def build():
    create_db()
    global core_path
    os.chdir(core_path)
    setup_file = os.path.join(core_path, "setup.py")
    subprocess.call(["python", setup_file, "build"])

def create_db():
    print(db_path)
    
    if not os.path.exists(db_path):
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        
        global ddl_path
        print(ddl_path)
        
        with open(ddl_path, 'r') as arquivo_sql:
            script = arquivo_sql.read()
            cursor.executescript(script)
            
        conexao.commit()
        
        with open(plc_List_path, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            for linha in leitor_csv:
                print("Gravando: ", linha)
                mlfb, type, descricao = linha
                cursor.execute("INSERT INTO CPU_List (mlfb, type, description) VALUES (?, ?, ?)", (mlfb, type, descricao))
        conexao.commit()
        conexao.close()
        
install_dependencies()
build()
