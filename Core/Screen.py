import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from repositories import UserConfig
from repositories import MlfbManagement
from Controller.OpennessController import open_project, chama_export

import Controller.OpennessController as OpennessController

# Criando a janela principal
root = tk.Tk()
root.geometry("600x400")
root.title("RPA Tia Openness")

# Variavel no nome do projeto
project_name_var=tk.StringVar()


############### FUNCTIONS ################

def CreateProject():
    project_name = project_name_var.get()
    
    if not UserConfig.CheckDll(151):
        label_status.config(text="Erro: Dll não configurada para esta versão do TIA")
        return
    
    if project_name != None and project_name != '' and project_dir != None and project_dir != '': 
        devices = []
        for linha in InfoHardware:
            devices.append({"HardwareType": linha["combobox"].get(), "Mlfb":linha["mlfb"].get(), "Name": linha["entry"].get()})   
        label_status.config(text="Criando projeto...")
        OpennessController.create_project(project_dir, project_name, devices)
    
    else:
        label_status.config(text="Erro: Nome do projeto ou diretório não informados")

def open_directory_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()
    
def open_file_dialog():
    return filedialog.askopenfilename()
    
def AddHardware():
    tupla_Input = {"combobox": tk.StringVar(root), "mlfb": tk.StringVar(root), "entry": tk.StringVar(root)}
    
    global NHardware
    
    def validate_device_name(event=None):
        new_device_name = tupla_Input["entry"].get()
        for info in InfoHardware:
            if info["entry"].get() == new_device_name and info is not tupla_Input:
                messagebox.showerror("Erro", "O nome do dispositivo já existe. Por favor, escolha um nome diferente.")
                tupla_Input["entry"].set('')  # Limpa o campo de entrada duplicado
                return False
        return True

    # Combobox 1º coluna
    combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["combobox"], values=opcoes_Hardware)
    combobox.grid(row=NHardware, column=0, padx=5)
    
    # MLFB - Combobox 2º coluna       
    mlfb_combobox = ttk.Combobox(screen_frames[4], textvariable=tupla_Input["mlfb"])
    mlfb_combobox.grid(row=NHardware, column=1, padx=5)
    
    def update_mlfb_combobox(*args):
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
    tupla_Input["combobox"].trace_add('write', update_mlfb_combobox)
    
    # Entry 3º coluna
    entry = ttk.Entry(screen_frames[4], textvariable=tupla_Input["entry"])
    entry.grid(row=NHardware, column=2, padx=5)
    
    # Adicione o callback de validação ao campo de entrada quando ele perder o foco ou quando a tecla Enter for pressionada
    entry.bind('<FocusOut>', validate_device_name)
    entry.bind('<Return>', validate_device_name)

    NHardware += 1
    
    InfoHardware.append(tupla_Input)


def update_status(status):
    global screen_instance
    if screen_instance:
        global RAP_status_Tela
        if not status:
            if RAP_status_Tela != OpennessController.RPA_status:
                RAP_status_Tela = OpennessController.RPA_status
        else:
            RAP_status_Tela = status
            
def setDllPath(dll_matrix):
    for dll in dll_matrix:
        tia_Version = dll["Tia_Version"]
        path = dll["Path"]
        UserConfig.saveDll(tia_Version, path)
    
def slice_tupla(string):
    if len(string) >= 2:
        return string[2:-3]
    else:
        return string
        
############### VARIABLES ################

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

############### SCREEN ################
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
        
        # Button Configurações
        BtnUserSettings = tk.Button(user_config, text="...", command=user_config_screen)
        BtnUserSettings.pack(padx=5, pady=5, anchor='w')
        screen_frames.append(BtnUserSettings)
        
        user_config.pack(padx=5, pady=5, anchor='w')
        
        proj_config_frame = ttk.Frame(root)
        screen_frames.append(proj_config_frame)
        
        # Project name
        ProjectName = tk.Label(proj_config_frame, text="Nome do projeto: ")
        ProjectName.grid(row=0, column=0, padx=5, pady=5)

        entrada1 = tk.Entry(proj_config_frame, textvariable = project_name_var)
        entrada1.grid(row=0, column=1, padx=5, pady=5)

        # Path
        btn_open_dialog = tk.Button(proj_config_frame, text="Selecionar diretório", command=open_directory_dialog)
        btn_open_dialog.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Button para criar
        criarBtn = tk.Button(proj_config_frame, text="Crair projeto", command=CreateProject)
        criarBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Button para abrir projeto
        criarBtn = tk.Button(proj_config_frame, text="Abrir projeto", command=open_project)
        criarBtn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Button para exportar bloco
        criarBtn = tk.Button(proj_config_frame, text="Export Blocks", command=chama_export)
        criarBtn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


        proj_config_frame.pack()

        # Button para adicionar uma nova linha
        botao_adicionar_linha = tk.Button(root, text="Adicionar hardware", command=AddHardware)
        botao_adicionar_linha.pack(pady=10)
        screen_frames.append(botao_adicionar_linha)

        hardwareConfig = ttk.Frame(root)
        hardwareConfig.pack(padx=5, pady=5)
        screen_frames.append(hardwareConfig)
        
        global RAP_status_Tela
        global label_status
        label_status = tk.Label(root, text="Nome do projeto: " + RAP_status_Tela)
        label_status.pack(padx=5, pady=5)

        root.mainloop()
        
def user_config_screen():
    usr_config_screen = tk.Toplevel(root)
    usr_config_screen.title("Configurações do usuário")
    usr_config_screen.geometry("540x360")
    
    usr_config_screen.transient(root)
    usr_config_screen.grab_set()
    
    nova_label = tk.Label(usr_config_screen, text="Aqui você pode configurar suas preferências")
    nova_label.pack()
    
    dll_config_frame = ttk.Frame(usr_config_screen)
    
    InstructionsDllPath = tk.Label(dll_config_frame, text="Indique o caminho das dlls:")
    InstructionsDllPath.grid(row=0, column=0, padx=5, pady=5)

    dll_matrix = []
    
    def setDllTuple(Tia_Version):
        
        info_dll = {"Tia_Version": Tia_Version, "Path": open_file_dialog()}
        dll_matrix.append(info_dll)
    
    # Tia V15.1
    label151 = tk.Label(dll_config_frame, text="Tia V15.1:")
    label151.grid(row=1, column=0, padx=5, pady=5)
    
    Btn151 = tk.Button(dll_config_frame, command=lambda: setDllTuple(151), width=10)
    Btn151.grid(row=1, column=1, padx=5, pady=5)    
    
    # Tia V16
    label16 = tk.Label(dll_config_frame, text="Tia V16:")
    label16.grid(row=2, column=0, padx=5, pady=5)
    
    Btn16 = tk.Button(dll_config_frame, command=lambda: setDllTuple(16), width=10)
    Btn16.grid(row=2, column=1, padx=5, pady=5)
    
    # Tia V17
    label17 = tk.Label(dll_config_frame, text="Tia V17:")
    label17.grid(row=3, column=0, padx=5, pady=5)
    
    Btn17 = tk.Button(dll_config_frame, command=lambda: setDllTuple(17), width=10)
    Btn17.grid(row=3, column=1, padx=5, pady=5,)
    
    dll_config_frame.pack(padx=5, pady=5)
    
    SaveConfirmations = tk.Button(usr_config_screen, text="Salvar", command=lambda: setDllPath(dll_matrix))
    SaveConfirmations.pack(padx=5, pady=5)
    
    fechar_botao = tk.Button(usr_config_screen, text="Fechar", command=usr_config_screen.destroy)
    fechar_botao.pack()
        
############### RENDER ################
main_screen()