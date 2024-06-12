import os
from Services import OpennessService
import traceback
from System.IO import FileInfo # type: ignore

RPA_status = ""
hardwareList = []
myproject = None

def create_project(project_path, project_name, hardware):

    project_dir = OpennessService.get_directory_info(project_path)
    
    try:
        
        global RPA_status
        RPA_status = 'Starting TIA UI'
        print(RPA_status)
        
        mytia = OpennessService.open_tia_ui()

        #Creating new project
        RPA_status = 'Creating project'
        print(RPA_status)
        
        global myproject
        myproject = mytia.Projects.Create(project_dir, project_name)

        deviceName = ''
        deviceMlfb = ''
        for device in hardware:
            deviceName = device["Name"]
            deviceMlfb = device["Mlfb"]
            deviceType = device["HardwareType"]
            
            hardwareList.append(OpennessService.addHardware(deviceType, deviceName, deviceMlfb, myproject))
            
        myproject.Save()
            
        
        mysubnet = OpennessService.SetSubnetName(myproject)
        
        ProfinetInterfaces = OpennessService.GetAllProfinetInterfaces(myproject)
        print("N de interfaces PROFINET: ", len(ProfinetInterfaces))
        
        for port in ProfinetInterfaces:
            node = port.Nodes[0]
            OpennessService.ConnectToSubnet(node, mysubnet)
            
        RPA_status = "Rede PROFINET configurada com sucesso!"
        
        myproject.Save()

        # Import blocks to the device
        for device in hardware:
            deviceName = device["Name"]
            import_block = OpennessService.verify_and_import(myproject, deviceName, r"C:\Users\gabri\Documents\PROJETOS\AX_padrao\db_falhar - Copia.txt", repetitions=3)
            print(import_block)
        myproject.Save()
        
        RPA_status = 'Project created successfully!'
        print(RPA_status)
        return

    except Exception as e:
        RPA_status = f'Error: {e}'
        print(RPA_status)
        return
    
def open_project(project_path):
    RPA_status = 'Opening project'
    print(RPA_status)
    try:
        global myproject
        myproject = OpennessService.open_project(project_path)
        RPA_status = 'Project opened successfully!'
        print(RPA_status)
        
    except Exception as e:
        RPA_status = f'Error opening project: {e}\n{traceback.format_exc()}'
        print(RPA_status)
        return

def export_Block(PlcSoftware):
    RPA_status = 'Exporting block'
    print(RPA_status)
    try:
        OpennessService.export_Fb(PlcSoftware)
    except Exception as e:
        RPA_status = 'Error exporting block: ', e
        print('Error exporting block: ', e)
        return
    
def export_data_type(cpu, data_type_name : str, data_type_path : str):
    RPA_status = 'Exporting data type'
    print(RPA_status)
    
    try:
        if cpu == None:
            global myproject
            cpu_list = OpennessService.get_all_devices(myproject)
            cpu = cpu_list[0]
            
        OpennessService.export_data_type(cpu, data_type_name, data_type_path)
    except Exception as e:
        RPA_status = 'Error exporting data type while in controller: ', e
        print(RPA_status)
        return
        
    