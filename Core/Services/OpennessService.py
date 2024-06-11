import os
import clr
from System.IO import DirectoryInfo, FileInfo  # type: ignore
from System import Type # type: ignore
from repositories import UserConfig
import xml.etree.ElementTree as ET
from xml.dom import minidom




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

def compilate_device(device):
    try:
        RPA_status = "Compiling something..."
        print(RPA_status)
        get_service(comp.ICompilable, device).Compile()
    except Exception as e:
        print('Error compiling device:', e)
        
def get_all_devices(myproject):
    try:
        devices = []
        for device in myproject.Devices:
            devices.append(device)
        return devices
    except Exception as e:
        print('Error getting all devices:', e)
        
def configurePath(path):
    return path.replace("/", "\\")

def get_directory_info(path):
    project_dir = configurePath(path)
    return DirectoryInfo(project_dir)

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
            deviceCPU = myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
            return deviceCPU
            
        elif deviceType == "HMI":
            RPA_status = 'Creating HMI: ', deviceName
            print(RPA_status)
            config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
            deviceHMI =  myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
            return deviceHMI

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
                    get_types(device)
                    network_interface_cpu = get_network_interface_CPU(device)
                    network_ports.append(network_interface_cpu)
                    
                elif (hardware_type == "HMI"):
                    network_interface_ihm = get_network_interface_HMI(device)
                    network_ports.append(network_interface_ihm)
                    
            else:
                RPA_status = 'Device' + str(device.GetAttribute("Name")) + ' is GSD: '
                print(RPA_status)
                
        return network_ports

    except Exception as e:
        RPA_status = 'Error getting PROFINET interfaces: ', e
        print(RPA_status)
        
def getCompositionPosition(deviceComposition):
    return deviceComposition.DeviceItems

def get_service(tipo, parent):
    try:
        network_interface_type = tipo
        getServiceMethod = parent.GetType().GetMethod("GetService").MakeGenericMethod(network_interface_type)
        return getServiceMethod.Invoke(parent, None)
    except Exception as e:
        RPA_status = 'Error getting service: ', e
        print(RPA_status)
        
def get_software(parent):
    try:
        parent = parent.DeviceItems[1]
        software_container = get_service(hwf.SoftwareContainer, parent)
        if not software_container:
            raise Exception("No SoftwareContainer found for device.")
        else:
            plc_software = software_container.Software
            if not plc_software:
                raise Exception("No PLC software found for device.")
            return software_container.Software
    except Exception as e:
        RPA_status = 'Error getting software container: ', e
        print(RPA_status)
        print("Name: ", str(parent.GetAttribute("Name")))
        print("Type: ", parent.GetType())
        
def get_network_interface_CPU(deviceComposition):
    cpu = getCompositionPosition(deviceComposition)[1].DeviceItems
    for option in cpu:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET interface_1":
            return get_service(hwf.NetworkInterface, option)
            
def get_network_interface_HMI(deviceComposition):
    hmi = getCompositionPosition(deviceComposition)[1].DeviceItems
    for option in hmi:
        optionName = option.GetAttribute("Name")
        if optionName == "PROFINET Interface_1":
            return get_service(hwf.NetworkInterface, option)
        
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

# Função para alterar o nome e número no XML
def alterar_xml(arquivo_xml, novo_nome, novo_numero):
    try:
        # Parsing do XML
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        # Encontrar e modificar elementos Name e Number dentro das tags de rastros
        for trace in root.findall(".//Trace"):
            for item in trace:
                if 'Name' in item.tag:
                    if item.text == "0073_Falhas":
                        print(f"Changing Name from {item.text} to {novo_nome}")
                        item.text = novo_nome
                elif 'Number' in item.tag:
                    if item.text == "73":
                        print(f"Changing Number from {item.text} to {novo_numero}")
                        item.text = str(novo_numero)

        # Salvando o arquivo XML modificado com formatação
        tree.write(arquivo_xml, encoding='utf-8', xml_declaration=True)

        print(f"XML saved with new Name and Number: {novo_nome}, {novo_numero}")

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except Exception as e:
        print(f"Unexpected error while modifying XML: {e}")
        
def extrair_nome_numero(arquivo_xml):
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        # Remover namespace do root
        for elem in root.iter():
            elem.tag = elem.tag.split('}', 1)[-1]

        # Encontrar elementos Name e Number
        name_element = root.find('.//Name')
        number_element = root.find('.//Number')

        nome_base = name_element.text if name_element is not None else ""
        numero_base = int(number_element.text) if number_element is not None else 0

        return nome_base, numero_base

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return "", 0
    except Exception as e:
        print(f"Unexpected error while extracting from XML: {e}")
        return "", 0

def analisar_xml(arquivo_xml):
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        # Remover namespace do root
        for elem in root.iter():
            elem.tag = elem.tag.split('}', 1)[-1]

        # Encontrar elementos Name e Number
        name_element = root.find('.//Name')
        number_element = root.find('.//Number')

        nome = name_element.text if name_element is not None else "Name element not found"
        numero = number_element.text if number_element is not None else "Number element not found"

        return nome, numero

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error while analyzing XML: {e}")
        return None, None

def verify_and_import(myproject, device_name, file_path, repetitions=0):
    try:
        # Verificar se o dispositivo existe no projeto
        device = next((d for d in myproject.Devices if d.Name == device_name), None)
        
        if not device:
            print(f"Device {device_name} not found in the project.")
            return

        # Acessar o serviço SoftwareContainer do item do dispositivo
        plc_software = get_software(device)

        # Extrair nome e número base do XML
        nome_base, numero_base = extrair_nome_numero(file_path)

        if not nome_base or not numero_base:
            print("Failed to extract base name or number from XML.")
            return

        # Função para importar os blocos de código para o software PLC
        def import_blocks():
            print(f"Importing block to CPU: {device_name}")
            import_options = tia.ImportOptions.Override
            graphic_file_info = FileInfo(file_path)
            blocos = plc_software.BlockGroup.Blocks.Import(graphic_file_info, import_options)
            print(blocos)

        # Executar a primeira importação
        import_blocks()

        # Executar importações adicionais conforme necessário
        for i in range(repetitions):
            print(f"Repetition {i+1} of {repetitions}")

            # Modificar o XML com novos valores de nome e número
            novo_nome = f"{int(nome_base.split('_')[0]) + i + 1:04d}_Falhas"
            novo_numero = numero_base + i + 1
            
            # Chamar a função para modificar o XML
            alterar_xml(file_path, novo_nome, novo_numero)

            # Realizar a importação após modificar o XML
            import_blocks()

    except Exception as e:
        print('Error verifying or importing file:', e)
        
def get_types(cpu):
    plc_software = get_software(cpu)
    type_group = plc_software.TypeGroup
    return type_group.Types 

def import_data_type(cpu, data_type_path):
    try:
        types = get_types(cpu)
        data_type_path = get_directory_info(data_type_path)
        
        types.Import(data_type_path, None, None)
    except Exception as e:
        print('Error importing data type:', e)
    
def export_data_type(cpu, data_type_name, data_type_path):
    try:
        types = get_types(cpu)
        data_type_path = get_directory_info(data_type_path)
        
        data_type = types.Find(data_type_name)
        if data_type is None:
            print("Data type not found")
            print(types.GetType())
            return
        elif data_type.GetAttribute("IsConsistent") == False:
            print("Type: ", data_type.GetType())
            print("Data type is not consistent")
            compilate_device(cpu)
        
        data_type.Export(data_type_path, tia.ExportOptions.WithDefaults)
    except Exception as e:
        print('Error exporting data type while in service:', e)	