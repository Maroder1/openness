import clr
from System.IO import DirectoryInfo

import os

clr.AddReference(r'C:\Program Files\Siemens\Automation\Portal V15_1\PublicAPI\V15.1\Siemens.Engineering.dll')
import Siemens.Engineering as tia

project_dir = 'C:\\Users\\Willian\\Desktop\\tia_python'


def create_project(project_path, project_name, hardware):
    
    project_path = DirectoryInfo (project_dir)
    
    #Starting TIA
    print ('Starting TIA with UI')
    mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)

    #Creating new project
    print ('Creating project')
    
    myproject = mytia.Projects.Create(project_path, project_name)

    for plc_Name in hardware:
        print ('Creating station')
        station_mlfb = 'OrderNumber:6ES7 518-4AP00-0AB0/V2.6'
        myproject.Devices.CreateWithItem(station_mlfb, plc_Name, plc_Name)
        
    print ('Project created successfully!')

    return