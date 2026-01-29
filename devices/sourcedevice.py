from devices.griddeviceclass import *
from generic.genericconfigwindowclass import *
from network.payloads.gridelementconfigs.sourceconfig import SourceConfig
from auxillary.typeinfo import *

class GridSource(GridDevice):
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # init parent
        super().__init__(editor, editorPage, networkInterface, scopeManager)
        
        self.editor.AppendDevice(self)
        
        # basic data
        self.portType = "none"
        
        self.deviceConfig = 0
    
    def Delete(self):
        # delete parent and remove device from editor
        super().Delete()
        
        self.editor.RemoveDevice(self)
        
        return
    
    def CreateNewSource(self, posX, posY):
        # create a new converter from a generic config file
        configData = self.CreateBlankFromTypeFile("templates/source.json", posX, posY, 0)
        
        self.deviceType = DeviceType.SOURCE
        
        return
    
    def CreateNewSourceFromFile(self, config, gridFile):
        # generate a new instance
        self.CreateFromFileConfigData("templates/source.json", gridFile, config)
        
        # store config data into class
        self.deviceName = config["name"]
        
        self.deviceType = DeviceType.SOURCE
        self.deviceID = config["deviceID"]
        
        # get connection types
        self.portType = self.graphicalElementHandler.connectionList[0].type
        
        # set visual appearance
        if self.portType[-2:].lower() == "ac":
            self.graphicalElementHandler.graphicalElementsDict["grid_type"].SetText("~")
        else:
            self.graphicalElementHandler.graphicalElementsDict["grid_type"].SetText("=")
        
        # update name in editor window
        self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
        
        return
    
    @staticmethod
    def CreateDeviceGridConfiguration(config):
        # get data from device
        #print (config)
        id = config["deviceID"]
        pointId = config["connections"]["0"]["pointID"]
        posX = config["positionX"]
        posY = config["positionY"]
        rotation = config["rotation"]
        name = config["name"]
        
        return SourceConfig(id, pointId, posX, posY, rotation, name)
    
    @staticmethod
    def CreateFileConfigFromGridConfiguration(payload):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "source"
        deviceConfig["positionX"] = payload.posX
        deviceConfig["positionY"] = payload.posY
        deviceConfig["rotation"] = payload.rotation
        
        # fill in device configuration
        deviceConfig["name"] = payload.name
        deviceConfig["deviceID"] = payload.id
        
        pointIDs = [payload.pointId]

        connData = {}
        
        connData["pointID"] = pointIDs[0]
        
        connectionConfig[str(0)] = connData
        
        # append config to base data
        deviceConfig["connections"] = connectionConfig
        
        return deviceConfig
    
    # function for creating a dictionary of the device configuration
    def GenerateSaveToFileData(self, gridFile):
        # create empty dictionary
        deviceConfig = {}
        connectionConfig = {}
        
        # fill in basic data
        deviceConfig["type"] = "source"
        deviceConfig["positionX"] = self.graphicalElementHandler.posX
        deviceConfig["positionY"] = self.graphicalElementHandler.posY
        deviceConfig["rotation"] = self.graphicalElementHandler.rotation
        
        # fill in device configuration
        deviceConfig["name"] = self.deviceName
        deviceConfig["deviceID"] = self.deviceID
        
        # fill in connection configuration
        # create new dict
        connData = {}
        
        # get the point of the connection
        connPoint = self.graphicalElementHandler.connectionList[0].connectionPoint
        
        connData["positionX"] = connPoint.posX
        connData["positionY"] = connPoint.posY
        connData["pointID"] = connPoint.id
        connData["electricalType"] = connPoint.type
        
        connectionConfig[str(0)] = connData
        
        # append config to base data
        deviceConfig["connections"] = connectionConfig
        
        return deviceConfig
    
    # function to show either configuration window or control window
    def ShowControlConfigWindow(self, mode):
        # depending on the mode, show either the control or the config window
        if mode == "editor":
            # create the configuration for the config window
            config = {}
            config["Source Name"] = GenericTextConfig(init=self.deviceName, maxLength=19).GetConfig()
            config["Source Type"] = GenericDropDownConfig(init=self.portType, values=GetTypeList()).GetConfig()
            
            # show the configuration menu
            converterConfigWindow = GenericConfigurationWindow(self.editor.window, config, self._OnConfigWindowReturn)
            converterConfigWindow.title("Source Configuration")
            converterConfigWindow.wait_window()
        
        return
    
    def _OnConfigWindowReturn(self, config):
        # store config of device
        self.deviceName = config["Source Name"]
        
        # set the type of the connection points
        if self.graphicalElementHandler.connectionList[0].SetType(config["Source Type"]):
            self.portType = config["Source Type"]
            
            # set visual appearance
            if self.portType[-2:].lower() == "ac":
                self.graphicalElementHandler.graphicalElementsDict["grid_type"].SetText("~")
            else:
                self.graphicalElementHandler.graphicalElementsDict["grid_type"].SetText("=")
        
        # update name in editor window
        self.graphicalElementHandler.graphicalElementsDict["Name"].SetText(self.deviceName)
        
        return