import os
import shutil
import clr
from repositories import UserConfig
from System.IO import DirectoryInfo

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

project_dir = ""
mytia = None

RPA_status = ""

def set_project_dir(path):
    global project_dir
    project_dir = path.replace("/", "\\")

def create_project(project_path, project_name, hardware):
    
    set_project_dir(project_path)
    
    try:
        project_path = DirectoryInfo (project_dir)
        
        #Starting TIA
        global RPA_status
        RPA_status = 'Starting TIA UI'
        print(RPA_status)
        
        global mytia
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

        #Creating new project
        RPA_status = 'Creating project'
        print(RPA_status)
        
        myproject = mytia.Projects.Create(project_path, project_name)

        deviceName = ''
        deviceMlfb = ''
        for device in hardware:
            deviceName = device["Name"]
            deviceMlfb = device["Mlfb"]

            if device["HardwareType"] == "PLC":
                RPA_status = 'Creating CPU: ', deviceName
                print(RPA_status)
                config_Plc = "OrderNumber:"+deviceMlfb+"/V1.6"
                myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
                
            elif device["HardwareType"] == "HMI":
                RPA_status = 'Creating HMI: ', deviceName
                print(RPA_status)
                config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
                myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
            
            elif device["HardwareType"] == "IO Node":
                RPA_status = 'Creating IO Node: ', deviceName
                print(RPA_status)
                confing_IOnode = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
                myproject.Devices.CreateWithItem(confing_IOnode, deviceName, deviceName)
                
            else:
                RPA_status = 'Unknown hardware type: ', device["HardwareType"]
                print(RPA_status)
            
        RPA_status = 'Project created successfully!'
        print(RPA_status)

        return

    except Exception as e:
        RPA_status = 'Error: ', e
        print(RPA_status)
        return
        
    