import os
import clr
from System.IO import DirectoryInfo, FileInfo
from System import Type
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
    project_path = configurePath(project_path)
    file_info = FileInfo(project_path)
    
    if not file_info.Exists:
        print("Project file not found:", project_path)
        return None
    projects = tia.TiaPortal(tia.ProjectComposition.OpenWithUpgrade(project_path))
    return projects

def addHardware(deviceType, deviceName, deviceMlfb, myproject):
    try:
        if deviceType == "PLC":
            print('Creating CPU: ', deviceName)
            config_Plc = "OrderNumber:"+deviceMlfb+"/V1.6"
            return myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
            
        elif deviceType == "HMI":
            RPA_status = 'Creating HMI: ', deviceName
            print(RPA_status)
            config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
            return myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)

        elif deviceType == "IO Node":
            RPA_status = 'Creating IO Node: ', deviceName
            print(RPA_status)
            confing_IOnode = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
            return myproject.Devices.CreateWithItem(confing_IOnode, deviceName, deviceName)
            
    except Exception as e:
        RPA_status = 'Unknown hardware type: ', deviceType
        print(RPA_status)
        RPA_status = 'Error creating hardware: ', e
        print(RPA_status)
        
def GetAllProfinetInterfaces(myproject):
    RPA_status = 'Getting PROFINET interfaces'
    print(RPA_status)
    try:
        network_ports = []
        for device in myproject.Devices:
            if (not is_gsd(device)):
                hardware_type = getHardwareType(device)
                
                if (hardware_type == "CPU"):
                    network_interface = get_network_interface_CPU(device)
                    network_ports.append(network_interface)
                    
                elif (hardware_type == "HMI"):
                    network_interface = get_network_interface_HMI(device)
                    network_ports.append(network_interface)
                    
            else:
                RPA_status = 'Device' + device.GetAttribute("Name") + ' is GSD: '
                print(RPA_status)
                
        return network_ports

    except Exception as e:
        RPA_status = 'Error getting PROFINET interfaces: ', e
        print(RPA_status)
        
def getCompositionPosition2(deviceComposition):
    return deviceComposition.DeviceItems[1]
        
def get_network_interface_CPU(deviceComposition):
    cpu = getCompositionPosition2(deviceComposition).DeviceItems
    for option in cpu:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET interface_1":
            network_interface_type = hwf.NetworkInterface
            getServiceMethod = option.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
            return getServiceMethod.Invoke(option, None)
            
def get_network_interface_HMI(deviceComposition):
    hmi = getCompositionPosition2(deviceComposition)
    print("HMI")
        
def is_gsd(device):
    try:
        if device.GetAttribute("IsGsd") == True:
            return True
        return False
    except Exception as e:
        RPA_status = 'Error checking GSD: ', e
        print(RPA_status)
        
def is_cpu(device):
    try:
        if str(device.GetAttribute("Classification")) == "CPU":
            return True
        return False
    except Exception as e:
        RPA_status = 'Error checking CPU: ', e
        print(RPA_status)
        
def getHardwareType(device):
    try:
        device_item_impl = getCompositionPosition2(device)
        if (is_cpu(device_item_impl)):
            return "CPU"
        else:
            print("Não é CPU")
    except Exception as e:
        RPA_status = 'Error getting hardware type: ', e
        print(RPA_status)

def ConnectToSubnet(node, subnet):
    try:
        RPA_status = 'Connecting to subnet'
        node.ConnectToSubnet(subnet)
    except Exception as e:
        RPA_status = 'Error connecting to subnet: ', e
        print(RPA_status)
        
def SetSubnetName(myproject):
    RPA_status = 'Setting subnet name'
    print(RPA_status)
    return myproject.Subnets.Create("System:Subnet.Ethernet", "NewSubnet")    
    
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