import clr
from System.IO import DirectoryInfo
clr.AddReference(r'C:\Program Files\Siemens\Automation\Portal V15_1\PublicAPI\V15.1\Siemens.Engineering.dll')

import os

import Siemens.Engineering as tia
import Siemens.Engineering.HW.Features as hwf
import Siemens.Engineering.Compiler as comp

project_dir = 'C:\\Users\\Willian\\Desktop\\tia_python'
mytia = None


def create_project(project_path, project_name, hardware):
    
    project_path = DirectoryInfo (project_dir)
    
    #Starting TIA
    print ('Starting TIA with UI')
    global mytia
    mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

    #Creating new project
    print ('Creating project')
    
    myproject = mytia.Projects.Create(project_path, project_name)

    deviceName = ''
    for device in hardware:
        deviceName = device["Name"]

        if device["HardwareType"] == "PLC":
            print ('Creating CPU: ', deviceName)
            config_Plc = 'OrderNumber:6ES7 518-4AP00-0AB0/V2.6'
            myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
            
        else:
            if device["HardwareType"] == "HMI":
                print ('Creating HMI: ', deviceName)
                config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
                myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
        
    print ('Project created successfully!')

    return