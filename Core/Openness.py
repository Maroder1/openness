import clr
from System.IO import DirectoryInfo
clr.AddReference(r'C:\Program Files\Siemens\Automation\Portal V15_1\PublicAPI\V15.1\Siemens.Engineering.dll')
import os

import Siemens.Engineering as tia
import Siemens.Engineering.HW.Features as hwf
import Siemens.Engineering.Compiler as comp

project_dir = 'C:\\Users\\Willian\\Desktop\\tia_python'
mytia = None

RPA_status = ""

def create_project(project_path, project_name, hardware):
    
    try:
        project_path = DirectoryInfo (project_dir)
        
        #Starting TIA
        global RPA_status
        RPA_status = 'Starting TIA UI'
        
        global mytia
        mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

        #Creating new project
        RPA_status = 'Creating project'
        
        myproject = mytia.Projects.Create(project_path, project_name)

        deviceName = ''
        for device in hardware:
            deviceName = device["Name"]

            if device["HardwareType"] == "PLC":
                RPA_status = 'Creating CPU: ', deviceName
                config_Plc = 'OrderNumber:6ES7 518-4AP00-0AB0/V2.6'
                myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
                
            elif device["HardwareType"] == "HMI":
                RPA_status = 'Creating HMI: ', deviceName
                config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
                myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
            
            elif device["HardwareType"] == "IO Node":
                RPA_status = 'Creating IO Node: ', deviceName
                confing_IOnode = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
                myproject.Devices.CreateWithItem(confing_IOnode, deviceName, deviceName)
                
            else:
                RPA_status = 'Unknown hardware type: ', device["HardwareType"]
            
        RPA_status = 'Project created successfully!'

        return

    except Exception as e:
        RPA_status = 'Error: ', e
        return
        
    