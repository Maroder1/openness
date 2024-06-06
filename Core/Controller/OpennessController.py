from Services import OpennessService

RPA_status = ""
hardwareList = []

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
            
            hardwareList.append(OpennessService.addHardware(deviceType, deviceName, deviceMlfb, myproject))
            
        myproject.Save()
            
        RPA_status = 'Project created successfully!'
        print(RPA_status)
        
        mysubnet = OpennessService.SetSubnetName(myproject)
        print(RPA_status)
        
        network_ports = OpennessService.GetAllProfinetInterfaces(myproject)
        
        for port in network_ports:
            OpennessService.ConnectToSubnet(port.Nodes[0], mysubnet)
        
        return

    except Exception as e:
        RPA_status = 'Error: ', e
        print(RPA_status)
        return
    
def open_project(path):
    RPA_status = 'Opening project'
    print(RPA_status)
    try:
        mokedPath = r'C:\Users\Willian\Documents\Automation\Factory_IO\PickNPlace_V15.1\PickNPlace_V15.1.ap15_1'
        path = mokedPath
        projeto = OpennessService.open_project(path)
        print(projeto)
        export_Block(projeto)
    except Exception as e:
        RPA_status = 'Error opening project: ', e
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
        
    