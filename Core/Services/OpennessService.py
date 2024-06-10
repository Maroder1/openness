import os
import clr
from System.IO import DirectoryInfo, FileInfo  # type: ignore
from System import Type # type: ignore
from repositories import UserConfig




def add_DLL(tia_Version):
    try:
        tuple = UserConfig.getDllPath(tia_Version)
        if tuple is None:
            print(f"Não foi possível obter o caminho da DLL para a versão {tia_Version}.")
            return False
        
        project_dll = r'' + tuple[0]
        clr.AddReference(project_dll)
        
        global tia, hwf, comp

        import Siemens.Engineering as tia # type: ignore
        import Siemens.Engineering.HW.Features as hwf # type: ignore
        import Siemens.Engineering.Compiler as comp # type: ignore

        print('DLL reference added successfully!')
        return True

    except Exception as e:
        print("Error adding DLL reference: ", e)
        return False
def open_tia_ui():
    # Create an instance of Tia Portal
    return tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

def configurePath(path):
    return path.replace("/", "\\")

def get_directory_info(path):
    project_dir = configurePath(path)
    return DirectoryInfo (project_dir)

def get_file_info(path):
    path = configurePath(path)
    return FileInfo(path)
    
def open_project(project_path):
    file_info = get_file_info(project_path)
    
    if not file_info.Exists:
        print("Project file not found:", project_path)
        return None
    mytia = open_tia_ui()
    return mytia.Projects.Open(file_info)

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
                    network_interface_cpu = get_network_interface_CPU(device)
                    network_ports.append(network_interface_cpu)
                    
                elif (hardware_type == "HMI"):
                    network_interface_ihm = get_network_interface_HMI(device)
                    network_ports.append(network_interface_ihm)
                    
            else:
                RPA_status = 'Device' + device.GetAttribute("Name") + ' is GSD: '
                print(RPA_status)
                
        return network_ports

    except Exception as e:
        RPA_status = 'Error getting PROFINET interfaces: ', e
        print(RPA_status)
        
def getCompositionPosition(deviceComposition):
    return deviceComposition.DeviceItems
        
def get_network_interface_CPU(deviceComposition):
    cpu = getCompositionPosition(deviceComposition)[1].DeviceItems
    for option in cpu:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET interface_1":
            network_interface_type = hwf.NetworkInterface
            getServiceMethod = option.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
            return getServiceMethod.Invoke(option, None)
            
def get_network_interface_HMI(deviceComposition):
    hmi = getCompositionPosition(deviceComposition)[1].DeviceItems
    for option in hmi:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET Interface_1":
            network_interface_type = hwf.NetworkInterface
            getServiceMethod = option.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
            return getServiceMethod.Invoke(option, None)
        
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
        device_item = device[1]
        if str(device_item.GetAttribute("Classification")) == "CPU":
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking CPU: ', e
        print(RPA_status)

def is_hmi(device):
    try:
        device_item = device[0]
        type_identifier = str(device_item.GetAttribute("TypeIdentifier"))
        
        if (type_identifier.__contains__("OrderNumber:6AV")):
            return True
        return False
    
    except Exception as e:
        RPA_status = 'Error checking HMI: ', e
        print(RPA_status)
        
def getHardwareType(device):
    try:
        device_item_impl = getCompositionPosition(device)
        if (is_cpu(device_item_impl)):
            return "CPU"
        elif (is_hmi(device_item_impl)):
            return "HMI"
            
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


#(TiaPortal.Projects[0].Devices[0].DeviceItems[1].GetService<SoftwareContainer>().Software as PlcSoftware).BlockGroup.Blocks


def verify_and_import(myproject, device_name, file_path):
    try:
        # Verificar se o dispositivo existe no projeto
        device = next((d for d in myproject.Devices if d.Name == device_name), None)
        
        if not device:
            print(f"Device {device_name} not found in the project.")
            return

        # Acessar o serviço SoftwareContainer do item do dispositivo
        software_container = device.DeviceItems[1].GetService[hwf.SoftwareContainer]()
        
        if not software_container:
            print(f"No SoftwareContainer found for device {device_name}.")
            return

        # Acessar o software PLC do contêiner de software
        plc_software = software_container.Software
        
        if not plc_software:
            print(f"No PLC software found for device {device_name}.")
            return

        # Importar os blocos de código para o software PLC
        print(f"Importing block to CPU: {device_name}")
        import_options = tia.ImportOptions.Override
        graphic_file_info = FileInfo(file_path)
        blocos = plc_software.BlockGroup.Blocks.Import(graphic_file_info, import_options)
        print(blocos)

    except Exception as e:
        print('Error verifying or importing file:', e)


