import os
import clr
from System.IO import DirectoryInfo, FileInfo
from repositories import UserConfig


def add_DLL(tia_Version):
    try:
        tuple = UserConfig.getDllPath(tia_Version)
        project_dll = r'' + tuple[0]
        clr.AddReference(project_dll)
        
        global tia
        global hwf
        global comp

        import Siemens.Engineering as tia
        import Siemens.Engineering.HW.Features as hwf
        import Siemens.Engineering.Compiler as comp

        RPA_status = 'DLL reference added successfully!'
        print(RPA_status)

    except Exception as e:
        print ("Error adding DLL reference: ")
        RPA_status = str(e)
        print(RPA_status)
        
if UserConfig.CheckDll(151):
    add_DLL(151)
    
def create_project():
    return tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

def set_project_dir(path):
    project_dir = configurePath(path)
    return DirectoryInfo (project_dir)

def configurePath(path):
    return path.replace("/", "\\")

def open_project(project_path):
    projects = tia.TiaPortal.Projects
    return projects

def addHardware(deviceType, deviceName, deviceMlfb, myproject):
    if deviceType == "PLC":
        print('Creating CPU: ', deviceName)
        config_Plc = "OrderNumber:"+deviceMlfb+"/V1.6"
        myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
        
    elif deviceType == "HMI":
        RPA_status = 'Creating HMI: ', deviceName
        print(RPA_status)
        config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
        myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
    
    elif deviceType == "IO Node":
        RPA_status = 'Creating IO Node: ', deviceName
        print(RPA_status)
        confing_IOnode = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
        myproject.Devices.CreateWithItem(confing_IOnode, deviceName, deviceName)
        
    else:
        RPA_status = 'Unknown hardware type: ', deviceType
        print(RPA_status)
        
def export_Fb(PlcSoftware):
    
    Block = PlcSoftware.BlockGroup.Blocks.Find("MyBlock")
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Define o caminho da pasta "exportados"
    caminho_pasta = os.path.join(diretorio_atual, 'exportados')

    # Define o caminho do arquivo dentro da pasta "exportados"
    caminho_arquivo = os.path.join(caminho_pasta, 'nome_do_arquivo.txt')
    
    with open(caminho_arquivo, 'w') as arquivo:
        # Escreve alguma coisa no arquivo
        arquivo.write(Block.Name)
    
    # Block.Export(new FileInfo(string.Format(@”D:\Samples\{0}.xml”, Block.Name)),
    # # # ExportOptions.WithDefaults);