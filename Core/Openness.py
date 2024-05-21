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
    global myproject
    myproject = mytia.Projects.Create(project_path, project_name)

    for str in hardware:
        CriaPlc(str)
    
    #Addding Stations
    print ('Creating station 1')
    station1_mlfb = 'OrderNumber:6ES7 515-2AM01-0AB0/V2.6'
    station1 = myproject.Devices.CreateWithItem(station1_mlfb, 'station1', 'station1')

    print ('Creating station 2')
    station2_mlfb = 'OrderNumber:6ES7 518-4AP00-0AB0/V2.6'
    station2 = myproject.Devices.CreateWithItem(station2_mlfb, 'station2', 'station2')

    return

def CriaPlc (plc_name):
    global myproject
    plc_mlfb = 'OrderNumber:6ES7 151-1AA05-0AB0/V2.6'
    plc = myproject.Devices.CreateWithItem(plc_mlfb, plc_name, plc_name)
    return

############### CAMPOS ################
myproject = None