import os
import csv
import sqlite3

current_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_path, "Openness.db")

def create_db():
    
    core_path = os.path.dirname(current_path)
    ddl_path = os.path.join(core_path, "Database", "ddl.sql")
    plc_List_path = os.path.join(core_path, "Database", "mlfb", "PLC_List.csv")
    
    print("")
    print("Db path: ", db_path)
    print("DDL path: ", ddl_path)
    
    if not os.path.exists(db_path):
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        
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