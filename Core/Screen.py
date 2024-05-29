import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk 

from repositories import UserConfig
from repositories import MlfbManagement

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
    project_name = project_name_var.get()
    
    devices = []
    for linha in InfoHardware:
        devices.append({"HardwareType": linha["combobox"].get(), "Mlfb":linha["mlfb"].get(), "Name": linha["entry"].get()})
        
    update_status("Creating project...")
    Openness.create_project(project_dir, project_name, devices)
    update_status(None)
    # root.destroy()
    
# Caixa de dialogo
def open_file_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()
    
def adicionar_linha():
    
    tupla_Input = {"combobox": tk.StringVar(root), "mlfb": tk.StringVar(root), "entry": tk.StringVar(root)}
    
    global NHardware
    
    # Combobox 1º coluna
    combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["combobox"], values=opcoes_Hardware)
    combobox.grid(row=NHardware, column=0, padx=5)
    
    # MLFB - Combobox 2º coluna       
    mlfb_combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["mlfb"])
    mlfb_combobox.grid(row=NHardware, column=1, padx=5)
    
    def update_mlfb_combobox(event):
        selected_option = tupla_Input["combobox"].get()

        if selected_option == "PLC":
            valueSource = mlfb_List[0]
        elif selected_option == "HMI":
            valueSource = mlfb_List[1]
        elif selected_option == "IO Node":
            valueSource = mlfb_List[2]
        else:
            valueSource = []

        mlfb_combobox['values'] = valueSource
    
    # Vincule a função de atualização da combobox à combobox principal
    tupla_Input["combobox"].trace_add('write', lambda *args: update_mlfb_combobox(None))
    
    # Entry 2º coluna
    entry = ttk.Entry(screen_frames[4], textvariable=tupla_Input["entry"])
    entry.grid(row=NHardware, column=2, padx=5)
    
    NHardware += 1
    
    InfoHardware.append(tupla_Input)


def update_status(status):
    global screen_instance
    if screen_instance:
        global RAP_status_Tela
        if not status:
            if RAP_status_Tela != Openness.RPA_status:
                RAP_status_Tela = Openness.RPA_status
        else:
            RAP_status_Tela = status
            
def setDllPath(dll_matrix):
    for dll in dll_matrix:
        print(dll)
        # UserConfig.saveDll(dll[0], dll[1])
    
def slice_tupla(string):
    if len(string) >= 2:
        return string[2:-3]
    else:
        return string
        
############### Valoriaveis ################

project_dir = None
NHardware = 0
InfoHardware = []
RAP_status_Tela = "Idle"
screen_instance = False
screen_frames = []
opcoes_Hardware = ["PLC", "HMI", "IO Node"]

mlfb_Plc = []
mlfb_ihm = []
mlfb_npde = []

mlfb_List=[mlfb_Plc, mlfb_ihm, mlfb_npde]

############### TELA ################
def main_screen():
    global screen_frames
    
    global screen_instance
    if not screen_instance:
        screen_instance = True
        update_status("Idle")
        
        i=0
        for type in opcoes_Hardware:
            for ii in MlfbManagement.getMlfbByHwType(type):
                mlfb_List[i].append(slice_tupla(str(ii)))
            i += 1
        
        #Frame for user configuration 
        user_config = ttk.Frame(root)
        screen_frames.append(user_config)
        
        # Botão Configurações
        botao_config = tk.Button(user_config, text="...", command=user_config_screen)
        botao_config.pack(padx=5, pady=5, anchor='w')
        screen_frames.append(botao_config)
        
        user_config.pack(padx=5, pady=5, anchor='w')
        
        proj_config_frame = ttk.Frame(root)
        screen_frames.append(proj_config_frame)
        
        # Nome do projeto
        label = tk.Label(proj_config_frame, text="Nome do projeto: ")
        label.grid(row=0, column=0, padx=5, pady=5)

        entrada1 = tk.Entry(proj_config_frame, textvariable = project_name_var)
        entrada1.grid(row=0, column=1, padx=5, pady=5)

        # Endereço projeto
        btn_open_dialog = tk.Button(proj_config_frame, text="Selecionar diretório", command=open_file_dialog)
        btn_open_dialog.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Botão para criar
        criarBtn = tk.Button(proj_config_frame, text="Crair projeto", command=Criar)
        criarBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        proj_config_frame.pack()

        # Botão para adicionar uma nova linha
        botao_adicionar_linha = tk.Button(root, text="Adicionar hardware", command=adicionar_linha)
        botao_adicionar_linha.pack(pady=10)
        screen_frames.append(botao_adicionar_linha)

        hardwareConfig = ttk.Frame(root)
        hardwareConfig.pack(padx=5, pady=5)
        screen_frames.append(hardwareConfig)
        
        global RAP_status_Tela
        label_status = tk.Label(root, text="Nome do projeto: " + RAP_status_Tela)
        label_status.pack(padx=5, pady=5)

        root.mainloop()
        
def user_config_screen():
    usr_config_screen = tk.Toplevel(root)
    usr_config_screen.title("Configurações do usuário")
    usr_config_screen.geometry("540x360")
    
    nova_label = tk.Label(usr_config_screen, text="Aqui você pode configurar suas preferências")
    nova_label.pack()
    
    dll_config_frame = ttk.Frame(usr_config_screen)

    dll_matrix = []
    
    # Tia V15.1
    label151 = tk.Label(dll_config_frame, text="Tia V15.1:")
    label151.grid(row=0, column=0, padx=5, pady=5)
    
    input151 = tk.Entry(dll_config_frame)
    input151.grid(row=0, column=1, padx=5, pady=5)
    
    info_dll151 = {"Tia_Version": 151, "Path": input151.get()}
    dll_matrix.append(info_dll151)
    
    
    # Tia V16
    label16 = tk.Label(dll_config_frame, text="Tia V16:")
    label16.grid(row=1, column=0, padx=5, pady=5)
    
    input16 = tk.Entry(dll_config_frame)
    input16.grid(row=1, column=1, padx=5, pady=5)

    info_dll16 = {"Tia_Version": 16, "Path": input16.get()}
    dll_matrix.append(info_dll16)
    
    # Tia V17
    label17 = tk.Label(dll_config_frame, text="Tia V17:")
    label17.grid(row=2, column=0, padx=5, pady=5)
    
    input17 = tk.Entry(dll_config_frame)
    input17.grid(row=2, column=1, padx=5, pady=5)

    info_dll17 = {"Tia_Version": 151, "Path": input17.get()}
    dll_matrix.append(info_dll17)
    
    salvar = tk.Button(dll_config_frame, text="Salvar", command=lambda: setDllPath(dll_matrix))
    salvar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    
    dll_config_frame.pack(padx=5, pady=5)
    
    
    # Define um botão para fechar a nova janela
    fechar_botao = tk.Button(usr_config_screen, text="Fechar", command=usr_config_screen.destroy)
    fechar_botao.pack()
        
############### RENDER ################
main_screen()