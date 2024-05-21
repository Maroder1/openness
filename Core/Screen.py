import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk 

import Openness

# Criando a janela principal
root = tk.Tk()
root.geometry("600x400")
root.title("MVP Tia Openness")

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
    
    # index_botao = botao_adicionar_linha.grid_info()
    print(botao_adicionar_linha.grid_info())
    nova_linha_frame.pack()
    
    linhas.append(nova_linha)
        
############### Valoriaveis ################

project_dir = None
linhas = []
opcoes_Hardware = ["PLC", "HMI"]

############### CAMPOS ################

# Nome do projeto
label = tk.Label(root, text="Nome do projeto: ")
label.pack(pady=20)  # pady é a margem vertical
entrada1 = tk.Entry(root, textvariable = project_name_var)
entrada1.pack()  # Adicione esta linha para exibir o campo de entrada

# Endereço projeto
btn_open_dialog = tk.Button(root, text="Selecionar diretóroi", command=open_file_dialog)
btn_open_dialog.pack(pady=10)

# Botão para adicionar uma nova linha
botao_adicionar_linha = tk.Button(root, text="Adicionar Linha", command=adicionar_linha)
botao_adicionar_linha.pack(pady=10)

# Botão para criar
criarBtn = tk.Button(root, text="Crair projeto", command=Criar)
criarBtn.pack()

# Executando o loop principal
root.mainloop()
