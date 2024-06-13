import os
import csv
import sqlite3

current_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_path, "Openness.db")
core_path = os.path.dirname(current_path)

def create_db():
    
    ddl_path = os.path.join(core_path, "Database", "ddl.sql")
    
    if not os.path.exists(db_path):
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        
        print(ddl_path)
        
        # Carrega o script SQL e executa
        with open(ddl_path, 'r') as arquivo_sql:
            script = arquivo_sql.read()
            cursor.executescript(script)
        conexao.commit()
        
        insert_cpu(conexao)
        insert_dll(conexao)
        conexao.close()


def insert_cpu(conexao):
    cursor = conexao.cursor()
    plc_List_path = os.path.join(core_path, "Database", "mlfb", "PLC_List.csv")
    print("Gravando dados na tabela CPU_List")
    with open(plc_List_path, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        for linha in leitor_csv:
            mlfb, type, descricao = linha
            cursor.execute("INSERT INTO CPU_List (mlfb, type, description) VALUES (?, ?, ?)", (mlfb, type, descricao))
    conexao.commit()


def insert_dll(conexao):
    cursor = conexao.cursor()
    print("Gravando dados na tabela Dll_Path")
    
    for versao in range(15, 19):
        if versao == 15:
            path = f"C:\\Program Files\\Siemens\\Automation\\Portal V15_1\\PublicAPI\\V15.1\\Siemens.Engineering.dll"
            cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (151, path))
        else:
            path = f"C:\\Program Files\\Siemens\\Automation\\Portal V{versao}\\PublicAPI\\V{versao}\\Siemens.Engineering.dll"
            cursor.execute("INSERT INTO Dll_Path (Tia_Version, Path) VALUES (?, ?)", (versao, path))
        print(path)
    conexao.commit()

def validate_db():
    if not os.path.exists(db_path):
        create_db()
        
    else:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM CPU_List")
        result = cursor.fetchone()
        if result[0] == 0:
            create_db()
        conexao.close()