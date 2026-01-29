from devices.griddeviceclass import *
from generic.genericconfigwindowclass import *
from network.payloads.gridelementconfigs.fenswitchgearconfig import FENSwitchgearConfig
from devices.fenswitchgearcontrolwindow import SwitchgearControlWindow
from network.packets.fenswitchgear import *
from network.packets.fenswitchgearrespond import *
from network.payloads.fenswitchgearrespond import *

class FENSwitchgearDevice(GridDevice):
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # call grid device init
        super().__init__(editor, editorPage, networkInterface, scopeManager)
        
        # create control window
        self.fenSwitchgearControlWindow = None
        
        # append to editor
        self.editor.AppendDevice(self)
        
    def Delete(self):
        # call grid device function
        super().Delete()
        
        # remove device from editor
        self.editor.RemoveDevice(self)
        
        return
    
    # this creates a new blank switchgear device
    def CreateNewFENSWitchgear(self, posX, posY):
        # first generate a new blank device
        configData = self.CreateBlankFromTypeFile("templates/fenSwitchgear.json", posX, posY, 0)
        
        self.deviceType = DeviceType.FENSWITCHGEAR
        #self.deviceID = self.editor.GetNewDeviceID()
        
        #self.editor.RegisterDeviceID(self.deviceType, self.deviceID, self)
        
        return
    
    # this creates a new switchgear from a file
    def CreateNewFENSWitchgearFromFile(self, config, gridFile):
        # generate a new instance
        self.CreateFromFileConfigData("templates/fenSwitchgear.json", gridFile, config)
        
        # store config data into class
        self.deviceIP = config["IP"]
        self.devicePort = config["port"]
        self.deviceName = config["name"]
        
        self.deviceType = DeviceType.FENSWITCHGEAR
        self.deviceID = config["deviceID"]
        
        #self.editor.RegisterDeviceID(self.deviceType, self.deviceID, self)
        
        return
    
    @staticmethod
    def CreateDeviceGridConfiguration(config):
        # get data from device
        print (config)
        id = config["deviceID"]
        point1Id = config["connections"]["0"]["pointID"]
        point2Id = config["connections"]["1"]["pointID"]
        point3Id = config["connections"]["2"]["pointID"]
        point4Id = config["connections"]["3"]["pointID"]
        port = config["port"]
        conf = 0
        ip = config["IP"]
        posX = config["positionX"]
        posY = config["positionY"]
        rotation = config["rotation"]
        rsvd = 0
        name = config["name"]
        
        return FENSwitchgearConfig(id, point1Id, point2Id, point3Id, point4Id, port, conf, ip, posX, posY, rotation, rsvd, name)
    
    @staticmethod
    def CreateFileConfigFromGridConfiguration(payload):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "fenSwitchgear"
        deviceConfig["positionX"] = payload.posX
        deviceConfig["positionY"] = payload.posY
        deviceConfig["rotation"] = payload.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = payload.ip
        deviceConfig["port"] = payload.port
        deviceConfig["name"] = payload.name
        deviceConfig["deviceID"] = payload.id
        
        pointIDs = [payload.point1Id, payload.point2Id, payload.point3Id, payload.point4Id]
        
        # fill in connection configuration
        for i in range(4):
            # create new dict
            connData = {}
            
            connData["pointID"] = pointIDs[i]
            
            connectionConfig[str(i)] = connData
        
        # append config to base data
        deviceConfig["connections"] = connectionConfig
        
        return deviceConfig
    
    # function for accepting a new incoming packet for this device
    def HandleNewPacket(self, packet):
        # hand the packet over to the network handler
        if isinstance(packet, FENSwitchgearLiveDataPacket):
            # extract data
            up = packet.payload.voltageP
            um = packet.payload.voltageM
            c1 = packet.payload.current1 - 1250
            c2 = packet.payload.current2 - 1250
            c3 = packet.payload.current3 - 1250
            c4 = packet.payload.current4 - 1250
            
            closedSwitches = packet.payload.closedSwitches
            
            online = False
            if packet.payload.deviceStatus & FENSwitchgearStatus.ONLINE:
                online = True
            
            if self.fenSwitchgearControlWindow:
                try:
                    self.fenSwitchgearControlWindow.UpdateData((up,um, c1,c2,c3,c4), online, closedSwitches)
                except:
                    pass
        else:
            # notify packet distributor
            id = packet.header.commandId
            self.packetDistributor.NewPacketData(id, packet)
        
        return
    
    # function for creating a dictionary of the device configuration
    def GenerateSaveToFileData(self, gridFile):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "fenSwitchgear"
        deviceConfig["positionX"] = self.graphicalElementHandler.posX
        deviceConfig["positionY"] = self.graphicalElementHandler.posY
        deviceConfig["rotation"] = self.graphicalElementHandler.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = self.deviceIP
        deviceConfig["port"] = self.devicePort
        deviceConfig["name"] = self.deviceName
        deviceConfig["deviceID"] = self.deviceID
        
        # fill in connection configuration
        for i in range(4):
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
    
    # function for setting a switch
    def SendSwitchCommand(self, switch, closed):
        switchMask = 0x1 << (switch - 1)
        if closed:
            # create a close switch packet
            id, packet = FENSwitchgearSetSwitchPacket.FromConfig(self.deviceID, switchMask)
            print ("Closing switch " + str(switch))
        else:
            id, packet = FENSwitchgearResetSwitchPacket.FromConfig(self.deviceID, switchMask)
            print ("Opening switch " + str(switch))
        
        result = self._SendData(id, packet)
        
        if not result:
            print ("Timeout")
        
        return
    
    def SendLiveDataCommand(self, onOff):
        if onOff:
            # turn on live data
            id, packet = FENSwitchgearLiveDataOnPacket.FromConfig(self.deviceID)
            
            result = self._SendData(id, packet)
            
            if not result:
                print ("Timeout")
            
            print ("Live data turned on")
        else:
            # turn on live data
            id, packet = FENSwitchgearLiveDataOffPacket.FromConfig(self.deviceID)
            
            result = self._SendData(id, packet)
            
            if not result:
                print ("Timeout")
            
            print ("Live data turned off")
        return
    
    # function to show either configuration window or control window
    def ShowControlConfigWindow(self, mode):
        # depending on the mode, show either the control or the config window
        if mode == "editor":
            # create the configuration for the config window
            config = {}
            config["Device Name"] = GenericTextConfig(init=self.deviceName, maxLength=19).GetConfig()
            config["Network IP"] = GenericIPConfig(init=self.deviceIP).GetConfig()
            config["Network Port"] = GenericIntConfig(init=self.devicePort, limitMin=1, limitMax=65535).GetConfig()
            
            # show the configuration menu
            fenSwitchgearConfigWindow = GenericConfigurationWindow(self.editor.window, config, self._OnConfigWindowReturn)
            fenSwitchgearConfigWindow.title("Switchgear Configuration")
            fenSwitchgearConfigWindow.wait_window()
            
        elif mode == "viewer":
            # show the control window
            if not self.fenSwitchgearControlWindow:
                config = {"name" : self.deviceName, "ip" : self.deviceIP, "port" : self.devicePort}
                self.fenSwitchgearControlWindow = SwitchgearControlWindow(self.editor.window, self, config)
            else:
                self.fenSwitchgearControlWindow.lift()
        
        return
    
    def _OnConfigWindowReturn(self, config):
        # store config of device
        self.deviceName = config["Device Name"]
        self.packetDistributor.name = self.deviceName
        self.deviceIP = config["Network IP"]
        self.devicePort = config["Network Port"]
        
        return
    
    def _SendData(self, id, packet):
        # notify packet distributor and send packet
        self.packetDistributor.RegisterTransfer(id)
        
        self.networkInterface.SendData(packet.GetBytes())
        
        # wait for return
        return self.packetDistributor.WaitForTransferComplete(id)