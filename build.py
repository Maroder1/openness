import subprocess
import sqlite3
import csv
import os

current_path = os.path.abspath(__file__)
core_path = os.path.join(os.path.dirname(current_path), "Core")
requirements_path = os.path.join(os.path.dirname(core_path), "Core", "requirements")
ddl_path = os.path.join(os.path.dirname(core_path), "Core", "Database", "ddl.sql")
plc_List_path = os.path.join(os.path.dirname(core_path), "Core", "Database", "mlfb", "PLC_List.csv")

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
     if not os.path.exists('Openness.db'):
        conexao = sqlite3.connect('Openness.db')
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
                mlfb, descricao = linha
                cursor.execute("INSERT INTO CPU_List (mlfb, description) VALUES (?, ?)", (mlfb, descricao))
        conexao.commit()
        conexao.close()
        
install_dependencies()
build()
