from devices.griddeviceclass import *
from generic.genericconfigwindowclass import *
from network.payloads.gridelementconfigs.scibreakbreakerconfig import SciBreakBreakerConfig
from devices.scibreakbreakercontrolwindow import SciBreakBreakerControlWindow
from network.packets.scibreakbreaker import *
from network.packets.scibreakbreakerrespond import *
from network.payloads.scibreakbreakerrespond import *

class SciBreakBreakerDevice(GridDevice):
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # call grid device init
        super().__init__(editor, editorPage, networkInterface, scopeManager)
        
        # create control window
        self.sciBreakBreakerControlWindow = None
        
        # append to editor
        self.editor.AppendDevice(self)
    
    def Delete(self):
        # call grid device function
        super().Delete()
        
        # remove device from editor
        self.editor.RemoveDevice(self)
        
        return
    
    # this creates a new blank breaker device
    def CreateNewSciBreakBreaker(self, posX, posY):
        # first generate a new blank device
        configData = self.CreateBlankFromTypeFile("templates/breaker.json", posX, posY, 0)
        
        self.deviceType = DeviceType.SCIBREAKBREAKER
        #self.deviceID = self.editor.GetNewDeviceID()
        
        #self.editor.RegisterDeviceID(self.deviceType, self.deviceID, self)
        
        return
    
    # this creates a new breaker from a file
    def CreateNewSciBreakBreakerFromFile(self, config, gridFile):
        # generate a new instance
        self.CreateFromFileConfigData("templates/breaker.json", gridFile, config)
        
        # store config data into class
        self.deviceIP = config["IP"]
        self.devicePort = config["port"]
        self.deviceName = config["name"]
        
        self.deviceType = DeviceType.SCIBREAKBREAKER
        self.deviceID = config["deviceID"]
        
        #self.editor.RegisterDeviceID(self.deviceType, self.deviceID, self)
        
        return
    
    @staticmethod
    def CreateDeviceGridConfiguration(config):
        # get data from device
        #print (config)
        id = config["deviceID"]
        point1Id = config["connections"]["0"]["pointID"]
        point2Id = config["connections"]["1"]["pointID"]
        port = config["port"]
        conf = 0
        ip = config["IP"]
        posX = config["positionX"]
        posY = config["positionY"]
        rotation = config["rotation"]
        rsvd = 0
        name = config["name"]
        
        return SciBreakBreakerConfig(id, point1Id, point2Id, port, conf, ip, posX, posY, rotation, rsvd, name)
    
    @staticmethod
    def CreateFileConfigFromGridConfiguration(payload):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "sciBreakBreaker"
        deviceConfig["positionX"] = payload.posX
        deviceConfig["positionY"] = payload.posY
        deviceConfig["rotation"] = payload.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = payload.ip
        deviceConfig["port"] = payload.port
        deviceConfig["name"] = payload.name
        deviceConfig["deviceID"] = payload.id
        
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
    
    # function for accepting a new incoming packet for this device
    def HandleNewPacket(self, packet):
        # hand the packet over to the network handler
        if isinstance(packet, SciBreakBreakerLiveDataPacket):
            # extract data
            if packet.payload.status & SciBreakBreakerStatus.ONLINE:
                self.online = True
            else:
                self.online = False
            
            if packet.payload.status & 0x0100:
                self.closedTop = False
            else:
                self.closedTop = True
            
            if packet.payload.status & 0x010000:
                self.closedBot = False
            else:
                self.closedBot = True
            
            # update data in control window if needed
            if self.sciBreakBreakerControlWindow:
                self.sciBreakBreakerControlWindow.UpdateData(packet.payload, self.online, [self.closedTop, self.closedBot])
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
        deviceConfig["type"] = "sciBreakBreaker"
        deviceConfig["positionX"] = self.graphicalElementHandler.posX
        deviceConfig["positionY"] = self.graphicalElementHandler.posY
        deviceConfig["rotation"] = self.graphicalElementHandler.rotation
        
        # fill in device configuration
        deviceConfig["IP"] = self.deviceIP
        deviceConfig["port"] = self.devicePort
        deviceConfig["name"] = self.deviceName
        deviceConfig["deviceID"] = self.deviceID
        
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
    
    # live data command
    def SendLiveDataCommand(self, onOff):
        if onOff:
            # turn on live data
            id, packet = SciBreakBreakerLiveDataOnPacket.FromConfig(self.deviceID)
            
            result = self._SendData(id, packet)
            
            if not result:
                print ("Timeout")
            
            print ("Live data turned on")
        else:
            # turn on live data
            id, packet = SciBreakBreakerLiveDataOffPacket.FromConfig(self.deviceID)
            
            result = self._SendData(id, packet)
            
            if not result:
                print ("Timeout")
            
            print ("Live data turned off")
        return
    
    # function for closing the breaker
    def SendSwitchCommand(self, closed):
        # send command here
        if closed:
            # send close command
            id, packet = SciBreakBreakerClosePacket.FromConfig(self.deviceID)
        else:
            # send open command
            id, packet = SciBreakBreakerOpenPacket.FromConfig(self.deviceID)
        
        result = self._SendData(id, packet)
        
        if not result:
            print ("Timeout")
        
        return
    
    def SendTurnOnCommand(self, on):
        # send command here
        if on:
            id, packet = SciBreakBreakerTurnOnPacket.FromConfig(self.deviceID)
        else:
            id, packet = SciBreakBreakerTurnOffPacket.FromConfig(self.deviceID)
        
        result = self._SendData(id, packet)
        
        if not result:
            print ("Timeout")
        
        return
    
    def SendSetTripLevelCommand(self, level):
        # create packet
        id, packet = SciBreakBreakerSetTripLevelPacket.FromConfig(self.deviceID, [level, 0,0,0])
        
        result = self._SendData(id, packet)
        
        if not result:
            print ("Timeout")
        
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
            fenSwitchgearConfigWindow.title("Breaker Configuration")
            fenSwitchgearConfigWindow.wait_window()
            
        elif mode == "viewer":
            # show the control window
            if not self.sciBreakBreakerControlWindow:
                config = {"name" : self.deviceName, "ip" : self.deviceIP, "port" : self.devicePort}
                self.sciBreakBreakerControlWindow = SciBreakBreakerControlWindow(self.editor.window, self, config)
            else:
                self.sciBreakBreakerControlWindow.lift()
        
        return
    
    def _OnConfigWindowReturn(self, config):
        # store config of device
        self.deviceName = config["Device Name"]
        self.packetDistributor.name = self.deviceName
        self.deviceIP = config["Network IP"]
        self.devicePort = config["Network Port"]
        
        self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
        
        return
    
    def _SendData(self, id, packet):
        # notify packet distributor and send packet
        self.packetDistributor.RegisterTransfer(id)
        
        self.networkInterface.SendData(packet.GetBytes())
        
        # wait for return
        return self.packetDistributor.WaitForTransferComplete(id)