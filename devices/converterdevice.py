from devices.griddeviceclass import *
from devices.convertercontrolwindow import *
from generic.genericconfigwindowclass import *
from network.payloads.gridelementconfigs.converterconfig import ConverterConfig
from network.packets.converter import *
from auxillary.typeinfo import *
from network.headers.convertercommand import *
from network.packets.converterrespond import *
from network.payloads.converterrespond import *

class ConverterDevice(GridDevice):
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # init parent
        super().__init__(editor, editorPage, networkInterface, scopeManager)
        
        self.converterControlWindow = None
        
        self.editor.AppendDevice(self)
        
        # basic data
        self.port1Type = "none"
        self.port2Type = "none"
        
        self.deviceConfig = 0
    
    def Delete(self):
        # delete parent and remove device from editor
        super().Delete()
        
        self.editor.RemoveDevice(self)
        
        return
    
    # function for accepting a new incoming packet for this device
    def HandleNewPacket(self, packet):
        # new packet for converter
        if isinstance(packet, ConverterLiveDataPacket):
            # extract data
            # adjust name tag
            if packet.payload.status & ConverterStatusBits.ONLINE:
                self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
            else:
                self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName + " (offline)")
            
            # forward the packet to the control window
            if self.converterControlWindow:
                try:
                    self.converterControlWindow.Update(packet.payload)
                except:
                    pass
            
        else:
            # notify packet distributor
            id = packet.header.commandId
            self.packetDistributor.NewPacketData(id, packet)
        
        return
    
    def SendLiveDataCommand(self, onOff):
        # create packets
        if onOff:
            id, packet = ConverterLiveDataOnPacket.FromConfig(self.deviceID)
        else:
            id, packet = ConverterLiveDataOffPacket.FromConfig(self.deviceID)
        
        # send
        result = self._SendData(id, packet)
        if not result:
            print ("Cannot turn on/off live data for converter")
            return False
        
        return True
    
    def SendOffCommand(self):
        # send an off command
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, ConverterModes.MODE_OFF)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendIdleCommand(self):
        # send an off command
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, ConverterModes.MODE_IDLE)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendResetCommand(self):
        # send an off command
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, ConverterModes.MODE_RESET)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendPrechargeCommand(self, side, mode):
        # update the mode config field
        converterMode = 0
        opMode = 0
        
        if side == 1:
            opMode = ConverterModes.MODE_PRECHARGE_1
            if mode == "voltage":
                converterMode = ConverterModes.MODE_VOLTAGE_CONTROL_1
            else:
                converterMode = ConverterModes.MODE_DROOP_CONTROL_1
        else:
            opMode = ConverterModes.MODE_PRECHARGE_2
            if mode == "voltage":
                converterMode = ConverterModes.MODE_VOLTAGE_CONTROL_2
            else:
                converterMode = ConverterModes.MODE_DROOP_CONTROL_2
        
        data = [converterMode, 0,0,0]
        
        # create update data packet
        print ("Sending precharge setpoints")
        id, updatePacket = ConverterUpdateDataPacket.FromConfig(self.deviceID, opMode, data)
        
        # send packet
        result = self._SendData(id, updatePacket)
        if not result:
            print ("Problem with updating the precharge setpoints")
            return False
        
        # change the mode
        print ("Sending precharge command")
        id, modePacket = ConverterSetModePacket.FromConfig(self.deviceID, opMode)
        
        # send packet
        result = self._SendData(id, modePacket)
        if not result:
            print ("Problem sending precharge command")
            return False
        
        return True
    
    def SendVoltageControlCommand(self, side):
        # determine op mode
        opMode = 0
        if side == 1:
            opMode = ConverterModes.MODE_VOLTAGE_CONTROL_1
        else:
            opMode = ConverterModes.MODE_VOLTAGE_CONTROL_2
        
        # create packet
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, opMode)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendDroopControlCommand(self, side):
        # determine op mode
        opMode = 0
        if side == 1:
            opMode = ConverterModes.MODE_DROOP_CONTROL_1
        else:
            opMode = ConverterModes.MODE_DROOP_CONTROL_2
        
        # create packet
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, opMode)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendPowerControlCommand(self):
        # create packet
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, ConverterModes.MODE_POWER_CONTROL)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendDischargeCommand(self, side):
        # determine op mode
        opMode = 0
        if side == 1:
            opMode = ConverterModes.MODE_DISCHARGE_1
        else:
            opMode = ConverterModes.MODE_DISCHARGE_2
        
        # create packet
        id, packet = ConverterSetModePacket.FromConfig(self.deviceID, opMode)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendVoltageControlParameters(self, side, voltage):
        # determine parameter set
        pSet = 0
        if side == 1:
            pSet = ConverterModes.MODE_VOLTAGE_CONTROL_1
        else:
            pSet = ConverterModes.MODE_VOLTAGE_CONTROL_2
        
        # setup data
        if voltage < 0:
            voltage = 0
        
        if voltage > 6000:
            voltage = 6000
        
        data = [voltage, 0,0,0]
        
        # create update packet
        id, packet = ConverterUpdateDataPacket.FromConfig(self.deviceID, pSet, data)
        
        # send packet
        print ("Voltage control setpoint ID is " + str(id))
        result = self._SendData(id, packet)
        if not result:
            print ("Broken voltage control setpoints")
            return False
        
        return True
    
    def SendDroopControlParameters(self, side, p1, p2, p3, p4):
        # determine parameter set
        pSet = 0
        if side == 1:
            pSet = ConverterModes.MODE_DROOP_CONTROL_1
        else:
            pSet = ConverterModes.MODE_DROOP_CONTROL_2
        
        # setup data
        data = [p1, p2, p3, p4]
        
        # create update packet
        id, packet = ConverterUpdateDataPacket.FromConfig(self.deviceID, pSet, data)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def SendPowerControlParameter(self, value):
        # setup data
        data = [value, 0,0,0]
        
        id, packet = ConverterUpdateDataPacket.FromConfig(self.deviceID, ConverterModes.MODE_POWER_CONTROL, data)
        
        # send packet
        result = self._SendData(id, packet)
        if not result:
            return False
        
        return True
    
    def CreateNewConverter(self, posX, posY):
        # create a new converter from a generic config file
        configData = self.CreateBlankFromTypeFile("templates/converter.json", posX, posY, 0)
        
        self.deviceType = DeviceType.CONVERTER
        
        return
    
    def CreateNewConverterFromFile(self, config, gridFile):
        # generate a new instance
        self.CreateFromFileConfigData("templates/converter.json", gridFile, config)
        
        # store config data into class
        self.deviceIP = config["IP"]
        self.devicePort = config["port"]
        self.deviceName = config["name"]
        
        self.deviceType = DeviceType.CONVERTER
        self.deviceID = config["deviceID"]
        self.deviceConfig = config["deviceConfig"]
        
        # get connection types
        self.port1Type = self.graphicalElementHandler.connectionList[0].type
        self.port2Type = self.graphicalElementHandler.connectionList[1].type
        
        # set visual appearance
        self.graphicalElementHandler.graphicalElementsDict["Port_1_Text"].SetText(self.port1Type[-2:])
        self.graphicalElementHandler.graphicalElementsDict["Port_2_Text"].SetText(self.port2Type[-2:])
        
        # update name in editor window
        self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
        
        return
    
    @staticmethod
    def CreateDeviceGridConfiguration(config):
        # get data from device
        #print (config)
        id = config["deviceID"]
        point1Id = config["connections"]["0"]["pointID"]
        point2Id = config["connections"]["1"]["pointID"]
        port = config["port"]
        conf = config["deviceConfig"]
        ip = config["IP"]
        posX = config["positionX"]
        posY = config["positionY"]
        rotation = config["rotation"]
        rsvd = 0
        name = config["name"]
        
        return ConverterConfig(id, point1Id, point2Id, conf, port, ip, posX, posY, rotation, name)
    
    @staticmethod
    def CreateFileConfigFromGridConfiguration(payload):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "converter"
        deviceConfig["positionX"] = payload.posX
        deviceConfig["positionY"] = payload.posY
        deviceConfig["rotation"] = payload.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = payload.ip
        deviceConfig["port"] = payload.port
        deviceConfig["name"] = payload.name
        deviceConfig["deviceID"] = payload.id
        deviceConfig["deviceConfig"] = payload.config
        
        pointIDs = [payload.point1Id, payload.point2Id]
        
        # fill in connection configuration
        for i in range(2):
            # create new dict
            connData = {}
            
            connData["pointID"] = pointIDs[i]
            
            connectionConfig[str(i)] = connData
        
        # append config to base data
        deviceConfig["connections"] = connectionConfig
        
        return deviceConfig
    
    # function for creating a dictionary of the device configuration
    def GenerateSaveToFileData(self, gridFile):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "converter"
        deviceConfig["positionX"] = self.graphicalElementHandler.posX
        deviceConfig["positionY"] = self.graphicalElementHandler.posY
        deviceConfig["rotation"] = self.graphicalElementHandler.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = self.deviceIP
        deviceConfig["port"] = self.devicePort
        deviceConfig["name"] = self.deviceName
        deviceConfig["deviceID"] = self.deviceID
        deviceConfig["deviceConfig"] = self.deviceConfig
        
        # fill in connection configuration
        for i in range(2):
            # create new dict
            connData = {}
            
            # get the point of the connection
            connPoint = self.graphicalElementHandler.connectionList[i].connectionPoint
            
            connData["positionX"] = connPoint.posX
            connData["positionY"] = connPoint.posY
            connData["pointID"] = connPoint.id
            connData["electricalType"] = connPoint.type
            
            connectionConfig[str(i)] = connData
        
        # append config to base data
        deviceConfig["connections"] = connectionConfig
        
        return deviceConfig
    
    # function to show either configuration window or control window
    def ShowControlConfigWindow(self, mode):
        # depending on the mode, show either the control or the config window
        if mode == "editor":
            # create the configuration for the config window
            config = {}
            config["Device Name"] = GenericTextConfig(init=self.deviceName, maxLength=19).GetConfig()
            config["Network IP"] = GenericIPConfig(init=self.deviceIP).GetConfig()
            config["Network Port"] = GenericIntConfig(init=self.devicePort, limitMin=1, limitMax=65535).GetConfig()
            config["Port 1 Type"] = GenericDropDownConfig(init=self.port1Type, values=GetTypeList()).GetConfig()
            config["Port 2 Type"] = GenericDropDownConfig(init=self.port2Type, values=GetTypeList()).GetConfig()
            config["Use ADS"] = GenericCheckboxConfig(init=(self.deviceConfig & ConverterConfigValues.CONFIG_USE_ADS)).GetConfig()
            
            # show the configuration menu
            converterConfigWindow = GenericConfigurationWindow(self.editor.window, config, self._OnConfigWindowReturn)
            converterConfigWindow.title("Converter Configuration")
            converterConfigWindow.wait_window()
            
        elif mode == "viewer":
            # show the control window
            if not self.converterControlWindow:
                config = {"name" : self.deviceName, "ip" : self.deviceIP, "port" : self.devicePort}
                self.converterControlWindow = ConverterControlWindow(self.editor.window, self, config, self.scopeManager)
            else:
                self.converterControlWindow.lift()
        
        return
    
    def _OnConfigWindowReturn(self, config):
        # store config of device
        self.deviceName = config["Device Name"]
        self.packetDistributor.name = self.deviceName
        self.deviceIP = config["Network IP"]
        self.devicePort = config["Network Port"]
        
        # set the type of the connection points
        if self.graphicalElementHandler.connectionList[0].SetType(config["Port 1 Type"]):
            self.port1Type = config["Port 1 Type"]
            
            # set visual appearance
            self.graphicalElementHandler.graphicalElementsDict["Port_1_Text"].SetText(self.port1Type[-2:])
        
        if self.graphicalElementHandler.connectionList[1].SetType(config["Port 2 Type"]):
            self.port2Type = config["Port 2 Type"]
            
            # set visual appearance
            self.graphicalElementHandler.graphicalElementsDict["Port_2_Text"].SetText(self.port2Type[-2:])
        
        # create the device config
        self.deviceConfig = 0
        if config["Use ADS"]:
            self.deviceConfig |= ConverterConfigValues.CONFIG_USE_ADS
        
        # update name in editor window
        self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
        
        return
    
    def _SendData(self, id, packet):
        # notify packet distributor and send packet
        self.packetDistributor.RegisterTransfer(id)
        
        self.networkInterface.SendData(packet.GetBytes())
        
        # wait for return
        return self.packetDistributor.WaitForTransferComplete(id)