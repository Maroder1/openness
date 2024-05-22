import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk 

import Openness

# Criando a janela principal
root = tk.Tk()
root.geometry("600x400")
root.title("RPA Tia Openness")

# Variavel no nome do projeto
project_name_var=tk.StringVar()

############### FUNÇÕES ################

# Função para fechar a janela
def Criar():
    print("Caminho do arquivo: ", project_dir)
    project_name = project_name_var.get()
    print("Nome do projeto: ", project_name)
    Openness.create_project(project_dir, project_name)
    root.destroy()

# Caixa de dialogo
def open_file_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()
    
def adicionar_linha():
    nova_linha = {"combobox": tk.StringVar(root), "entry": tk.StringVar(root)}
    nova_linha_frame = ttk.Frame(root)
    
    # Combobox na primeira coluna
    combobox = ttk.Combobox(nova_linha_frame, textvariable=nova_linha["combobox"], values=opcoes_Hardware)
    combobox.pack(side=tk.LEFT, padx=5)
    
    # Entry na segunda coluna
    entry = ttk.Entry(nova_linha_frame, textvariable=nova_linha["entry"])
    entry.pack(side=tk.LEFT, padx=5)
    
    nova_linha_frame.pack(padx=5, pady=5)
        
############### Valoriaveis ################

project_dir = None
opcoes_Hardware = ["PLC", "HMI"]

############### CAMPOS ################
config_frame = ttk.Frame(root)

# Nome do projeto
label = tk.Label(config_frame, text="Nome do projeto: ")
label.grid(row=0, column=0, padx=5, pady=5)

entrada1 = tk.Entry(config_frame, textvariable = project_name_var)
entrada1.grid(row=0, column=1, padx=5, pady=5)

# Endereço projeto
btn_open_dialog = tk.Button(config_frame, text="Selecionar diretóroi", command=open_file_dialog)
btn_open_dialog.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Botão para criar
criarBtn = tk.Button(config_frame, text="Crair projeto", command=Criar)
criarBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

config_frame.pack()

# Botão para adicionar uma nova linha
botao_adicionar_linha = tk.Button(root, text="Adicionar hardware", command=adicionar_linha)
botao_adicionar_linha.pack(pady=10)

# Executando o loop principal
root.mainloop()
