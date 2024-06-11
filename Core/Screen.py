import sys
sys.coinit_flags = 2
import tkinter as tk
from tkinter import filedialog, ttk 
from PIL import Image, ImageTk

from repositories import UserConfig
from repositories import MlfbManagement
from Controller.OpennessController import open_project, export_Block
from Services.OpennessService import add_DLL
import Controller.OpennessController as OpennessController

# Criando a janela principal
root = tk.Tk()
root.geometry("600x400")
root.title("RPA Tia Openness")

# Variavel no nome do projeto
project_name_var=tk.StringVar()
quant_rb_import=tk.IntVar()
quant_gp_import=tk.IntVar()


############### FUNCTIONS ################
def CreateProject():
    project_name = project_name_var.get()
    global selected_version
    if not UserConfig.CheckDll(selected_version):
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
        
def open_project():
    project_path = open_file_dialog()
    if project_path != None and project_path != '':
        RAP_status_Tela = "Abrindo projeto..."
        print(RAP_status_Tela)
        open_project(project_path)
    else:
        label_status.config(text="Erro: Projeto não selecionado")

def open_directory_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()
    print(f'Selecionou o diretório: {project_dir}')
    
def open_file_dialog():
    return filedialog.askopenfilename()
    
def AddHardware():
    
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
selected_version = None
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
        criarBtn = tk.Button(proj_config_frame, text="Export Blocks", command=import_blocks_screen)
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

        # Carregar a imagem
        img = Image.open("logo.jpg")
        img = img.resize((100, 100), Image.ANTIALIAS)  # Redimensionar a imagem conforme necessário
        img = ImageTk.PhotoImage(img)
        
        # Exibir a imagem
        label_image = tk.Label(root, image=img)
        label_image.image = img  # Mantém uma referência para evitar a coleta de lixo
        label_image.place(x=root.winfo_width() - 100, y=0)  # Posiciona no canto superior direito

        root.mainloop()
def set_version(version_select):
    global selected_version 
    if version_select == 151:
        selected_version = 151
        print("151")
    elif version_select == 16:
        selected_version = 16
        print("16")
    elif version_select == 17:
        selected_version = 17
        print("17")
    else:
        print("Versão não reconhecida.")
        return None
    
    if add_DLL(selected_version):
        print(f"Versão {selected_version} configurada com sucesso.")
    else:
        print(f"Falha ao configurar a versão {selected_version}.")
    return selected_version

def user_config_screen():
    usr_config_screen = tk.Toplevel(root)
    usr_config_screen.title("Configurações do usuário")
    usr_config_screen.geometry("540x360")
    
    usr_config_screen.transient(root)
    usr_config_screen.grab_set()
    
    nova_label = tk.Label(usr_config_screen, text="Aqui você pode configurar suas preferências")
    nova_label.pack()
    
    dll_config_frame = ttk.Frame(usr_config_screen)
    
    InstructionsDllPath = tk.Label(dll_config_frame, text="Selecione a versão do TIA Portal:")
    InstructionsDllPath.grid(row=0, column=0, padx=5, pady=5)

    dll_matrix = []
    
    def setDllTuple(Tia_Version):
        info_dll = {"Tia_Version": Tia_Version, "Path": open_file_dialog()}
        dll_matrix.append(info_dll)
    
    # Tia V15.1
    Btn151 = tk.Button(dll_config_frame, command=lambda: set_version(151), width=10, text="Tia V15.1")
    Btn151.grid(row=1, column=0, padx=5, pady=5)    
    
    # Tia V16
    Btn16 = tk.Button(dll_config_frame, command=lambda: set_version(16), width=10, text="Tia V16")
    Btn16.grid(row=2, column=0, padx=5, pady=5)
    
    # Tia V17
    Btn17 = tk.Button(dll_config_frame, command=lambda: set_version(17), width=10, text="Tia V17")
    Btn17.grid(row=3, column=0, padx=5, pady=5,)
    
    dll_config_frame.pack(padx=5, pady=5)
    
    SaveConfirmations = tk.Button(usr_config_screen, text="Salvar", command=lambda: setDllPath(dll_matrix))
    SaveConfirmations.pack(padx=5, pady=5)
    
    fechar_botao = tk.Button(usr_config_screen, text="Fechar", command=usr_config_screen.destroy)
    fechar_botao.pack()

def import_blocks_screen():
    import_config_frame = tk.Toplevel(root)
    import_config_frame.title("Configurações dos blocos")
    import_config_frame.geometry("600x200")

    import_config_frame.transient(root)
    import_config_frame.grab_set()
    
    nova_label = tk.Label(import_config_frame, text="Aqui você pode selecionar os blocos que deseja importar")
    nova_label.pack(pady=10)
    
    frame_blocks = tk.Frame(import_config_frame)
    frame_blocks.pack(pady=10)

    # Bloco do robo
    InstructionBlocks = tk.Label(frame_blocks, text="Quantidade de blocos do robo deseja importar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    entrada1 = tk.Entry(frame_blocks, textvariable=quant_rb_import)
    entrada1.grid(row=0, column=1, padx=2, pady=2)

    BtnRB = tk.Checkbutton(frame_blocks, text="Importar bloco do robo")
    BtnRB.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    # Bloco do grampo
    InstructionBlocks1 = tk.Label(frame_blocks, text="Quantidade de blocos do grampo deseja importar?")
    InstructionBlocks1.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    entrada2 = tk.Entry(frame_blocks, textvariable=quant_gp_import)
    entrada2.grid(row=1, column=1, padx=2, pady=2)

    BtnGP = tk.Checkbutton(frame_blocks, text="Importar bloco do grampo")
    BtnGP.grid(row=1, column=2, padx=5, pady=5, sticky='w')

    fechar_botao = tk.Button(import_config_frame, text="Fechar", command=import_config_frame.destroy)
    fechar_botao.pack(pady=20)

        
############### RENDER ################
main_screen()