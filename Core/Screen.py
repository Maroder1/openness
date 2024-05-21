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

############### FUNÇÕES ################

# Função para fechar a janela
def fechar_janela():
    root.destroy()

# Caixa de dialogo
def open_file_dialog():
    global folder
    folder = filedialog.askdirectory()
        
############### Valoriaveis ################

folder = None

############### CAMPOS ################

# Nome do projeto
label = tk.Label(root, text="Nome do projeto: ", font=("Arial", 24))
entrada1 = tk.Entry(root)
entrada1.pack()  # Adicione esta linha para exibir o campo de entrada
label.pack(pady=20)  # pady é a margem vertical

# Endereço projeto
btn_open_dialog = tk.Button(root, text="Selecionar Arquivo", command=open_file_dialog)
btn_open_dialog.pack(pady=10)

# Botão para fechar a janela
fechar_botao = tk.Button(root, text="Fechar", command=fechar_janela)
fechar_botao.pack()

# Executando o loop principal
root.mainloop()
