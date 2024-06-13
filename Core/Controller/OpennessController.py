from Services import OpennessService
import traceback
from System.IO import FileInfo # type: ignore
import tkinter as tk

RPA_status = ""
hardwareList = []
myproject = None

def create_project(project_path, project_name, hardware, rb_blocks_value, gp_blocks_value):
    
    try:
        
        global RPA_status
        RPA_status = 'Starting TIA UI'
        print(RPA_status)
        
        mytia = OpennessService.open_tia_ui()

        #Creating new project
        RPA_status = 'Creating project'
        print(RPA_status)
        
        global myproject
        myproject = OpennessService.create_project(mytia, project_path, project_name)

        if hardware != None and myproject != None:
            addHardware(hardware)
            wire_profniet()

        if rb_blocks_value > 0 : 
            for device in hardware:
                deviceName = device["Name"]
                tipo = 'robo'
                import_block = OpennessService.verify_and_import(myproject, deviceName, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\db_falhas.xml", repetitions= rb_blocks_value, tipo = tipo)
                print(import_block)

        if gp_blocks_value > 0:
            for device in hardware:
                deviceName = device["Name"]
                import_block = OpennessService.verify_and_import(myproject, deviceName, r"\\AXIS-SERVER\Users\Axis Server\Documents\xmls\fc_falhas.xml", repetitions=gp_blocks_value, tipo= '')
                print(import_block)

        myproject.Save()
        
        RPA_status = 'Project created successfully!'
        print(RPA_status)
        return

    except Exception as e:
        RPA_status = f'Error: {e}'
        print(RPA_status)
        return
    
 
def addHardware(hardware):
    deviceName = ''
    deviceMlfb = ''
    for device in hardware:
        deviceName = device["Name"]
        deviceMlfb = device["Mlfb"]
        deviceType = device["HardwareType"]
        
        hardwareList.append(OpennessService.addHardware(deviceType, deviceName, deviceMlfb, myproject))
    myproject.Save()
    
    
def wire_profniet():
    ProfinetInterfaces = OpennessService.GetAllProfinetInterfaces(myproject)
    print("N de interfaces PROFINET: ", len(ProfinetInterfaces))
    
    if len(ProfinetInterfaces) > 1:
        mysubnet = OpennessService.SetSubnetName(myproject)
        for port in ProfinetInterfaces:
            node = port.Nodes[0]
            OpennessService.ConnectToSubnet(node, mysubnet)
            
        myproject.Save()
            
        RPA_status = "Rede PROFINET configurada com sucesso!"
        print(RPA_status)
        
    else:
        RPA_status = "Número de interfaces PROFINET menor que 2"
        print(RPA_status)

    
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
        
    