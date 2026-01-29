from graphical.canvaselementclass import *
from graphical.connectionpointclass import *
from graphical.graphicalelementhandlerclass import *

from network.headers.header import DeviceType
from network.packetdistributor import *

import json

# base class for every grid device
class GridDevice:
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # every device has a graphical representation
        self.editor = editor
        self.editorPage = editorPage
        self.networkInterface = networkInterface
        self.graphicalElementHandler = None
        self.deviceNetworkHandler = None
        self.packetDistributor = PacketDistributor()
        self.scopeManager = scopeManager
        
        # generic device data
        self.deviceIP = "192.168.1.169"
        self.devicePort = 502
        self.deviceName = ""
        
        self.deviceType = DeviceType.NONE
        self.deviceID = -1
    
    # function to delete a grid device
    def Delete(self):
        # this is type specific
        return
    
    # function to create a blank device from a type definition file
    def CreateBlankFromTypeFile(self, filename, posX, posY, rotation):
        # check if we already created a element handler
        if self.graphicalElementHandler:
            return
        
        # open the config file and extract the config data
        with open(filename, 'r') as f:
            config = json.load(f)
        
        # split into graphical and connection
        graphical = config["graphical"]
        connections = config["connections"]
        
        # create element handler and load in graphical elements and connections
        self.graphicalElementHandler = GraphicalElementHandler(self, self.editorPage, posX, posY, rotation)
        self.graphicalElementHandler.LoadGraphicalElements(graphical)
        self.graphicalElementHandler.LoadConnections(None, connections, connections)
        
        return
    
    # function to create a defined device from stored file data
    def CreateFromFileConfigData(self, filename, gridFile, fileConfig):
        # check if we already created an element handler
        if self.graphicalElementHandler:
            return
        
        # open the config file and extract the graphical data
        with open(filename, 'r') as f:
            config = json.load(f)
        
        graphical = config["graphical"]
        baseConnectionConfig = config["connections"]
        
        # get the position of the device
        posX = fileConfig["positionX"]
        posY = fileConfig["positionY"]
        rotation = fileConfig["rotation"]
        deviceConnectionConfig = fileConfig["connections"]
        
        # create a blank device from the given template
        self.graphicalElementHandler = GraphicalElementHandler(self, self.editorPage, posX, posY, rotation)
        self.graphicalElementHandler.LoadGraphicalElements(graphical)
        self.graphicalElementHandler.LoadConnections(gridFile, baseConnectionConfig, deviceConnectionConfig)
        
        return
    
    # function to hand over a new packet
    def HandleNewPacket(self, packet : bytearray):
        # this is type specific
        return
    
    # function to save the device into a grid
    def GenerateSaveToFileData(self):
        # this is type specific
        return
    
    # function to show the configuration window of the device
    def ShowControlConfigWindow(self):
        # this is type specific
        return