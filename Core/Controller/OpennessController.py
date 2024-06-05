import os
from Services import OpennessService
import traceback
import subprocess
from System.IO import FileInfo # type: ignore

RPA_status = ""

def create_project(project_path, project_name, hardware):

    project_dir = OpennessService.set_project_dir(project_path)
    
    try:
        
        global RPA_status
        RPA_status = 'Starting TIA UI'
        print(RPA_status)
        
        mytia = OpennessService.create_project()

        #Creating new project
        RPA_status = 'Creating project'
        print(RPA_status)
        
        myproject = mytia.Projects.Create(project_dir, project_name)

        deviceName = ''
        deviceMlfb = ''
        for device in hardware:
            deviceName = device["Name"]
            deviceMlfb = device["Mlfb"]
            deviceType = device["HardwareType"]
            
            OpennessService.addHardware(deviceType, deviceName, deviceMlfb, myproject)
            
        myproject.Save()
            
        RPA_status = 'Project created successfully!'
        print(RPA_status)
        
        # Importing file
        try:
            myproject.BlockGroup.Blocks.Import(r"C:\Users\gabri\Documents\Automation\0071_Falhas.db")
            RPA_status = 'File imported successfully!'
        except Exception as import_error:
            RPA_status = 'Error importing file: {}'.format(import_error)
        
        print(RPA_status)
        
        OpennessService.AssignIp(myproject)
        RPA_status = 'IP assigned successfully!'
        
        # open_project()
        
        return

    except Exception as e:
        RPA_status = 'Error: ', e
        print(RPA_status)
        return
    
def open_project(path):
    RPA_status = 'Opening project'
    print(RPA_status)
    try:
        # Define o caminho do TIA Portal
        tia_portal_path = r"C:\Program Files\Siemens\Automation\Portal V16\Bin\Siemens.Automation.Portal.exe"
        
        # Verifica se o TIA Portal está instalado
        if not os.path.isfile(tia_portal_path):
            raise Exception("TIA Portal is not installed or the path is incorrect.")
        
        # Define o caminho do projeto
        project_path = r"C:\Users\gabri\Documents\PROJETOS\AX_padrao\RCK - F598\RCK - F598.ap16"
        
        # Abre o TIA Portal e o projeto
        print("Opening TIA Portal and project...")
        subprocess.Popen([tia_portal_path, project_path])
        
        print("Project opened successfully.")
    
        export_Block("-A110")
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
        
    