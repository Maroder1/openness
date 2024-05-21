import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog

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
        
############### Valoriaveis ################

project_dir = None

############### CAMPOS ################

# Nome do projeto
label = tk.Label(root, text="Nome do projeto: ", font=("Arial", 24))
entrada1 = tk.Entry(root, textvariable = project_name_var)
entrada1.pack()  # Adicione esta linha para exibir o campo de entrada
label.pack(pady=20)  # pady é a margem vertical

# Endereço projeto
btn_open_dialog = tk.Button(root, text="Selecionar Arquivo", command=open_file_dialog)
btn_open_dialog.pack(pady=10)

# Botão para fechar a janela
criarBtn = tk.Button(root, text="Crair projeto", command=Criar)
criarBtn.pack()

# Executando o loop principal
root.mainloop()
