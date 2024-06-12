import sys
sys.coinit_flags = 2
import pywinauto
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import pywinauto

from repositories import UserConfig
from repositories import MlfbManagement
from Controller.OpennessController import open_project, export_Block, export_data_type
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
dt_to_export = tk.StringVar()

############### FUNCTIONS ################
def CreateProject():
    project_name = project_name_var.get()
    global selected_version, project_dir
    if not UserConfig.CheckDll(selected_version):
        label_status.config(text="Erro: Dll não configurada para esta versão do TIA")
        return
    
    if not validate_all_device_names():
        label_status.config(text="Erro: Há nomes de dispositivos duplicados. Por favor, verifique.")
        return
    
    if project_name and project_dir: 
        devices = []
        for linha in InfoHardware:
            devices.append({"HardwareType": linha["combobox"].get(), "Mlfb":linha["mlfb"].get(), "Name": linha["entry"].get()})   
        label_status.config(text="Criando projeto...")
        OpennessController.create_project(project_dir, project_name, devices, rb_blocks_value, gp_blocks_value)
    
    else:
        label_status.config(text="Erro: Nome do projeto ou diretório não informados")
        
def opn_project():
    project_path = open_file_dialog()
    if project_path != None and project_path != '':
        open_project(project_path)
    else:
        label_status.config(text="Erro: Projeto não selecionado")

def open_directory_project_dialog():
    global project_dir
    project_dir = filedialog.askdirectory()

def open_directory_dialog():
    return filedialog.askdirectory()
    
def open_file_dialog():
    return filedialog.askopenfilename()

def validate_all_device_names():
    names_seen = {}
    all_names_valid = True
    for info in InfoHardware:
        device_name = info["entry"].get()
        if device_name in names_seen:
            info["entry"].set('')  # Limpa o campo de entrada duplicado
            messagebox.showerror("Erro", f"O nome do dispositivo '{device_name}' já existe. Por favor, escolha um nome diferente.")
            all_names_valid = False
        else:
            names_seen[device_name] = info["entry"]
    return all_names_valid
    
def AddHardware():
    tupla_Input = {"combobox": tk.StringVar(root), "mlfb": tk.StringVar(root), "entry": tk.StringVar(root)}
    
    global NHardware
    
    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

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
    
    # Adicione o callback para focar no próximo widget quando a tecla Enter for pressionada
    entry.bind('<Return>', focus_next_widget)

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
rb_blocks_value = 0
rb_import_state = 0
gp_blocks_value = 0
gp_import_state = 0

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
        btn_open_dialog = tk.Button(proj_config_frame, text="Selecionar diretório", command=open_directory_project_dialog)
        btn_open_dialog.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Button para criar
        criarBtn = tk.Button(proj_config_frame, text="Criar projeto", command=CreateProject)
        criarBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Button para abrir projeto
        openBtn = tk.Button(proj_config_frame, text="Abrir projeto", command=opn_project)
        openBtn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Button para exportar bloco
        exportBkBtn = tk.Button(proj_config_frame, text="Import Blocks", command=import_blocks_screen)
        exportBkBtn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Button para exportar udt
        exportDtBtn = tk.Button(proj_config_frame, text="Export Data Type", command=export_data_type_screen)
        exportDtBtn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

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
        load_image(root, r".\logo.PNG")

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
    # Carregar a imagem
    load_image(usr_config_screen, r".\logo.PNG")
    
def export_data_type_screen():
    data_type_config_screen = tk.Toplevel(root)
    data_type_config_screen.title("Configurações do usuário")
    data_type_config_screen.geometry("540x360")
    
    data_type_config_screen.transient(root)
    data_type_config_screen.grab_set()
    
    frame_dt = tk.Frame(data_type_config_screen)
    frame_dt.pack(pady=10)
    
    InstructionBlocks = tk.Label(frame_dt, text="Nome do data type que deseja exportar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5,)
    
    nome_dt = tk.Entry(frame_dt, textvariable=dt_to_export)
    nome_dt.grid(row=0, column=1, padx=5, pady=5)
    
    export_dt = tk.Button(frame_dt, text="Exportar", command=call_export_dt)
    export_dt.grid(row=1, column=1, columnspan=2 ,padx=5, pady=5)
    
def call_export_dt():
    dt_name = dt_to_export.get()
    export_data_type(None, dt_name, open_directory_dialog())

   


def import_blocks_screen():
    global rb_blocks_value, rb_import_state, gp_blocks_value, gp_import_state
    
    # Criando a janela
    import_config_frame = tk.Toplevel(root)
    import_config_frame.title("Configurações dos blocos")
    import_config_frame.geometry("540x200")

    import_config_frame.transient(root)
    import_config_frame.grab_set()
    
    # Label informativo
    nova_label = tk.Label(import_config_frame, text="Aqui você pode selecionar os blocos que deseja importar")
    nova_label.pack(pady=10)
    
    # Frame para os blocos
    frame_blocks = tk.Frame(import_config_frame)
    frame_blocks.pack(pady=10)

    # Adicione os elementos ao frame_blocks
    add_elements_to_frame(frame_blocks)

    # Botão para salvar configurações e fechar a janela
    save_btn = tk.Button(import_config_frame, text="Salvar Configurações", command=lambda: save_config(entrada1rb, entrada2gp, import_config_frame))
    save_btn.pack(pady=20)

def add_elements_to_frame(frame):
    global entrada1rb, entrada2gp
    
    # Bloco do robô
    InstructionBlocks = tk.Label(frame, text="Quantidade de blocos do robô deseja importar?")
    InstructionBlocks.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    entrada1rb = tk.Entry(frame)
    entrada1rb.insert(0, rb_blocks_value)  # Inserir o valor armazenado
    entrada1rb.grid(row=0, column=1, padx=2, pady=2)


    # Bloco do grampo
    InstructionBlocks1 = tk.Label(frame, text="Quantidade de blocos do grampo deseja importar?")
    InstructionBlocks1.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    entrada2gp = tk.Entry(frame)
    entrada2gp.insert(0, gp_blocks_value)  # Inserir o valor armazenado
    entrada2gp.grid(row=1, column=1, padx=2, pady=2)


def save_config(entrada1rb, entrada2gp, window):
    global rb_blocks_value, gp_blocks_value
    
    # Atualizar as variáveis globais com os valores atuais
    rb_blocks_value = int(entrada1rb.get())
    gp_blocks_value = int(entrada2gp.get())
    
    # Aqui você pode salvar esses dados em um arquivo, banco de dados, etc.
    with open("config_blocos.txt", "w") as file:
        file.write(f"Robô - Quantidade: {rb_blocks_value}\n")
        file.write(f"Grampo - Quantidade: {gp_blocks_value}\n")

    print("Configurações salvas com sucesso!")
    
    # Fecha a janela
    window.destroy()



def load_image(window, image_path):
    # Carregar a imagem
    img = Image.open(image_path)
    img = img.resize((125, 100))  # Redimensionar a imagem conforme necessário
    img = ImageTk.PhotoImage(img)
        
    # Exibir a imagem
    label_image = tk.Label(window, image=img)
    label_image.image = img  # Mantém uma referência para evitar a coleta de lixo
    label_image.place(x=window.winfo_width() - img.width(), y=0)

    # Atualizar a posição da imagem quando a largura da janela mudar
    def update_image_position(event):
        label_image.place(x=window.winfo_width() - img.width(), y=0)

    window.bind("<Configure>", update_image_position)
        
############### RENDER ################
main_screen()