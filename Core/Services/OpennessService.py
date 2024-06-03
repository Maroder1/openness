def set_project_dir(path):
    return path.replace("/", "\\")

def addHardware(deviceType, deviceName, deviceMlfb, myproject):
    if deviceType == "PLC":
        print('Creating CPU: ', deviceName)
        config_Plc = "OrderNumber:"+deviceMlfb+"/V1.6"
        myproject.Devices.CreateWithItem(config_Plc, deviceName, deviceName)
        
    elif deviceType == "HMI":
        RPA_status = 'Creating HMI: ', deviceName
        print(RPA_status)
        config_Hmi = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
        myproject.Devices.CreateWithItem(config_Hmi, deviceName, None)
    
    elif deviceType == "IO Node":
        RPA_status = 'Creating IO Node: ', deviceName
        print(RPA_status)
        confing_IOnode = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
        myproject.Devices.CreateWithItem(confing_IOnode, deviceName, deviceName)
        
    else:
        RPA_status = 'Unknown hardware type: ', deviceType
        print(RPA_status)