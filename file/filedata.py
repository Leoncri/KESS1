import json
from graphical.pointclass import *
from graphical.segmentclass import *

from file.nodeclass import *

from devices.fenswitchgeardeviceclass import *
from devices.converterdevice import *
from devices.sourcedevice import *
from devices.scibreakbreakerdeviceclass import *

from network.packets.gridconfig import *
from network.packetdistributor import *
from network.packets.genericrespond import GenericRespondPacket
from network.packets.gridconfigrespond import GridConfigSizeRespondPacket
from network.packets.gridconfigrespond import GridGetConfigRespondPacket
from network.headers.gridrespond import GridRespond
from network.payloads.gridelementconfigs import *

from generic.genericprogressbarwindowclass import *

from auxillary.versioninfo import VersionInfo

class GridFile:
    def __init__(self, editor, editorPage, networkInterface, scopeManager):
        # store parameters
        self.editor = editor
        self.editorPage = editorPage
        self.networkInterface = networkInterface
        self.scopeManager = scopeManager
        
        # command distributor
        self.packetDistributor = PacketDistributor()
        
        # lists for points, segments and elements
        self.nodeList = []
        self.pointList = []
        self.segmentList = []
        self.elementList = []
        self.gridConfigurationList = []
    
    def Clear(self):
        # clear all lists
        self.nodeList.clear()
        self.pointList.clear()
        self.segmentList.clear()
        self.elementList.clear()
        self.gridConfigurationList.clear()
        
        return
    
    def SaveToFile(self, filename, points, segments, elements, fileType):
        # start creating the file config data
        fileData = {}
        genericData = {}
        electricalData = {}
        
        # setup generic data
        genericData["fileType"] = fileType
        genericData["version"] = 1
        
        # setup electrical data
        self.editorPage.GeneratePointIDs()
        for p in points:
            index = points.index(p)
            electricalData["point_" + str(index)] = p.GenerateSaveToFileData(self)
        
        for s in segments:
            index = segments.index(s)
            electricalData["segment_" + str(index)] = s.GenerateSaveToFileData(self)
        
        for e in elements:
            index = elements.index(e)
            electricalData["element_" + str(index)] = e.GenerateSaveToFileData(self)
        
        # put file together and store
        fileData["genericData"] = genericData
        fileData["electricalData"] = electricalData
        
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(fileData, f, ensure_ascii=False, indent=4)
        
        return
    
    def OpenFromFile(self, filename):
        # clear lists
        self.Clear()
        
        # get file config data
        with open(filename, "r", encoding="utf-8") as f:
            fileData = json.load(f)
        
        # check file version and editor mode
        genericData = fileData["genericData"]
        version = genericData["version"]
        mode = genericData["fileType"]
        
        self.editorPage.ChangeToEditorMode()
        
        if version != 1:
            return False
        
        # start reading in file data
        electricalData = fileData["electricalData"]
        for k in electricalData:
            if k.startswith("point_"):
                # create a new point
                p = Point(self.editorPage, 0, 0, "none")
                p.GenerateFromFileData(electricalData[k], self)
                self.pointList.append(p)
            elif k.startswith("segment_"):
                # create a new segment
                s = Segment(self.editorPage)
                s.GenerateFromFileData(electricalData[k], self)
            elif k.startswith("element_"):
                # generate new elements
                element = electricalData[k]
                type = element["type"]
                
                if type == "fenSwitchgear":
                    # create a new switchgear
                    e = FENSwitchgearDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
                    e.CreateNewFENSWitchgearFromFile(element, self)
                
                elif type == "converter":
                    # create a new converter
                    e = ConverterDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
                    e.CreateNewConverterFromFile(element, self)
                
                elif type == "source":
                    # create a new soource
                    e = GridSource(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
                    e.CreateNewSourceFromFile(element, self)
                
                elif type == "sciBreakBreaker":
                    # create a new breaker
                    e = SciBreakBreakerDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
                    e.CreateNewSciBreakBreakerFromFile(element, self)
        
        return True
    
    def UploadToServer(self, filename, points, segments, elements):
        # clear lists
        self.Clear()
        
        # generate nodes
        self.GenerateNodes(points.copy())
        
        # save file
        self.SaveToFile(filename, points, segments, elements, "editor")
        
        # reopen file and get electrical configuration
        with open(filename, "r", encoding="utf-8") as f:
            fileData = json.load(f)
        
        self.uploadData = fileData["electricalData"]
        
        # create a progress bar window
        progressWindow = GenericProgressBarWindow(self.editor.window, self._UploadDataToServer, "Uploading data")
        progressWindow.wait_window()
        
        return progressWindow.result
    
    def DownloadFromServer(self, filename):
        # clear lists
        self.Clear()
        
        # create a progress bar window
        progressWindow = GenericProgressBarWindow(self.editor.window, self._DownloadFromServer, "Downloading data")
        progressWindow.wait_window()
        print ("Progress bar window result: " + str(progressWindow.result))
        
        return progressWindow.result
    
    def NewPacket(self, packet):
        # get command id from packet
        commandId = packet.header.commandId
        self.packetDistributor.NewPacketData(commandId, packet)
        return
    
    def GetPointFromId(self, id):
        # iterate over all points and check for id
        for p in self.pointList:
            if p.id == id:
                return p
        
        return None
    
    def GenerateNodes(self, pointList):
        # this generates nodes from a point list
        nodeIDCounter = 1;
        while len(pointList) > 0:
            # let first point build a list of connected points
            start = pointList[0]
            
            cl = start.BuildConnectedPointsList([])
            
            # remove cl list elements and create new node
            for e in cl:
                pointList.remove(e)
            
            print ("Creating new node with id " + str(nodeIDCounter))
            type = cl[0].type
            self.nodeList.append(Node(nodeIDCounter, cl, type))
            nodeIDCounter += 1
        
        return
    
    def GenerateServerConfigurationData(self, electricalData):
        # create nodes first
        for n in self.nodeList:
            self.gridConfigurationList.append(n.CreateNodeGridConfiguration())
        
        # iterate over all elements in electrical configuration and create config as well
        for key in electricalData:
            if key.startswith("point_"):
                self.gridConfigurationList.append(Point.CreatePointGridConfiguration(electricalData[key]))
            elif key.startswith("segment_"):
                self.gridConfigurationList.append(Segment.CreateSegmentGridConfiguration(electricalData[key]))
            elif key.startswith("element_"):
                type = electricalData[key]["type"]
                print (type)
                if type == "fenSwitchgear":
                    self.gridConfigurationList.append(FENSwitchgearDevice.CreateDeviceGridConfiguration(electricalData[key]))
                elif type == "converter":
                    self.gridConfigurationList.append(ConverterDevice.CreateDeviceGridConfiguration(electricalData[key]))
                elif type == "source":
                    self.gridConfigurationList.append(GridSource.CreateDeviceGridConfiguration(electricalData[key]))
                elif type == "sciBreakBreaker":
                    self.gridConfigurationList.append(SciBreakBreakerDevice.CreateDeviceGridConfiguration(electricalData[key]))
        
        return
    
    # WARNING: This function locks itself for a certain time
    def ClearServerConfiguration(self):
        # send a clear server config packet and wait for a success
        id, packet = GridClearPacket.FromConfig()
        
        # wait for server to respond
        result = self._SendPacket(id, packet)
        
        if not result:
            return False
        
        if not isinstance(result, GenericRespondPacket):
            print ("Receiving bad packet as respond")
            return False
        
        if result.header.result == GridRespond.SUCCESS:
            return True
        
        return False
    
    # WARNING: This function locks itself for a certain time
    def UploadServerConfiguration(self, progressWindow):
        # set version for now
        version = VersionInfo(1,1)
        
        # get packets from grid config
        id, packetList = GridConfigPacket.FromConfig(self.gridConfigurationList, version)
        #print (packetList)
        
        percentPerPacket = 50 / len(packetList)
        counter = 1
        
        for p in packetList:
            # set progress
            progressWindow.SetProgress(percentPerPacket * (counter - 1) + 30, "Uploading " + str(counter) + "/" + str(len(packetList)) + " ...")
            
            # send every packet and wait for respond
            result = self._SendPacket(id, p)
        
            if not result:
                return False
        
            if not isinstance(result, GenericRespondPacket):
                print ("Receiving bad packet as respond")
                return False
            
            counter += 1
        
        return True
    
    def LoadServerConfiguration(self):
        # send a setup server packet
        id, packet = GridSetupPacket.FromConfig()
        
        result = self._SendPacket(id, packet)
        
        if not result:
            return False
        
        if not isinstance(result, GenericRespondPacket):
            print ("Receiving bad packet as respond")
            return False
        
        if result.header.result == GridRespond.SUCCESS:
            return True
        
        return False
    
    def GetServerConfiguration(self, progressWindow):
        # start with getting the amount of incoming configuration packets
        id, packet = GridGetConfigSizePacket.FromConfig()
        
        result = self._SendPacket(id, packet)
        
        if not result:
            return False
        
        if not isinstance(result, GridConfigSizeRespondPacket):
            print ("Receiving bad packet as respond")
            return False
        
        # get number of packets
        num = result.payload.numPackets
        if num == 0:
            print ("Receiving bad respond packet")
            return False
        
        print ("Number of packets: " + str(num))
        
        # ask server for configuration
        id, packet = GridGetConfigPacket.FromConfig()
        
        self.packetDistributor.RegisterMultipleTransfers(id)
        
        self.networkInterface.SendData(packet.GetBytes())
        
        result = self.packetDistributor.WaitForMultipleTransfersComplete(id, num)
        print (result)
        
        # check length of packets received
        if len(result) != num:
            print ("Received wrong number of configuration packets")
            return False
        
        # store elements in lists
        for p in result:
            if not isinstance(p, GridGetConfigRespondPacket):
                print ("Received bad respond packet")
            
            self.gridConfigurationList += p.payload.gridElementConfigList
        
        return True
    
    def ProcessServerConfiguration(self):
        # iterate over all received elements and create new objects
        for e in self.gridConfigurationList:
            if isinstance(e, NodeConfig):
                # create a new node
                self._CreateNewNode(e)
            elif isinstance(e, PointConfig):
                # create a new point
                self._CreateNewPoint(e)
            elif isinstance(e, SegmentConfig):
                # create a new segment
                self._CreateNewSegment(e)
            elif isinstance(e, FENSwitchgearConfig):
                # create a new switchgear
                self._CreateNewFENSwitchgear(e)
            elif isinstance(e, ConverterConfig):
                # create a new converter
                self._CreateNewConverter(e)
            elif isinstance(e, SourceConfig):
                # create a new source
                self._CreateNewSource(e)
            elif isinstance(e, SciBreakBreakerConfig):
                # create a new breaker
                self._CreateNewSciBreakBreaker(e)
        
        return
    
    def GetPointFromId(self, pointID):
        for p in self.pointList:
            if p.id == pointID:
                return p
        
        print ("Cannot find point with ID")
        
        return
    
    def _SendPacket(self, id, packet):
        # send a packet and wait for a respond
        self.packetDistributor.RegisterTransfer(id)
        print (packet.GetBytes().hex())
        self.networkInterface.SendData(packet.GetBytes())
        
        # wait for server to respond
        result = self.packetDistributor.WaitForTransferComplete(id)
        
        return result
    
    def _UploadDataToServer(self, progressWindow):
        # setup progressWindow
        progressWindow.SetProgress(0, "Creating configuration from file...")
        
        # generate server data from nodes and electrical data
        self.GenerateServerConfigurationData(self.uploadData)
        
        progressWindow.SetProgress(20, "Clearing server configuration...")
        
        # clear server configuration
        result = self.ClearServerConfiguration()
        if not result:
            progressWindow.ShowError("Upload Error", "Cannot clear server configuration.")
            progressWindow.SetReturnVariable(False)
            progressWindow.Finished()
            return
        
        progressWindow.SetProgress(30, "Uploading server configuration...")
        
        # send configuration to server
        result = self.UploadServerConfiguration(progressWindow)
        if not result:
            progressWindow.ShowError("Upload Error", "Cannot upload server configuration.")
            progressWindow.SetReturnVariable(False)
            progressWindow.Finished()
            return
        
        progressWindow.SetProgress(80, "Loading server configuration...")
        
        # let the server load in the new configuration
        result = self.LoadServerConfiguration()
        if not result:
            progressWindow.ShowError("Upload Error", "Cannot load server configuration.")
            progressWindow.SetReturnVariable(False)
            progressWindow.Finished()
            return
        
        progressWindow.SetProgress(100, "Server configuration uploaded")
        
        progressWindow.ShowInfo("Uploading Data", "Data successfully uploaded.")
        progressWindow.SetReturnVariable(True)
        progressWindow.Finished()
        return
    
    def _DownloadFromServer(self, progressWindow):
        # start with setting up the progress bar
        progressWindow.SetProgress(0, "Getting number of configuration packets...")
        
        # get the configuration from the server
        result = self.GetServerConfiguration(progressWindow)
        if not result:
            progressWindow.ShowError("Download Error", "Cannot download grid configuration from server.")
            progressWindow.SetReturnVariable(False)
            progressWindow.Finished()
            return
        
        progressWindow.SetProgress(80, "Processing downloaded data...")
        
        # process configuration data and fill lists
        self.ProcessServerConfiguration()
        
        progressWindow.SetProgress(100, "Server configuration downloaded")
        
        progressWindow.ShowInfo("Downloading data", "Data successfully downloaded.")
        progressWindow.SetReturnVariable(True)
        progressWindow.Finished()
        return
    
    def _CreateNewNode(self, config):
        # create a new node from config
        self.nodeList.append(Node.CreateNodeFromGridConfiguration(config))
        return
    
    def _CreateNewPoint(self, config):
        # create a new point
        posX = config.posX
        posY = config.posY
        id = config.id
        
        # search for node
        type = "none"
        nodeID = config.nodeId
        for e in self.nodeList:
            if e.id == id:
                type = e.type
        
        p = Point(self.editorPage, posX, posY, type)
        p.id = id
        self.pointList.append(p)
        return
    
    def _CreateNewSegment(self, config):
        # create a new segment
        point1Id = config.point1Id
        point2Id = config.point2Id
        
        point1 = self.GetPointFromId(point1Id)
        point2 = self.GetPointFromId(point2Id)
        
        s = Segment(self.editorPage)
        self.segmentList.append(s)
        
        point1.ConnectSegment(s)
        point2.ConnectSegment(s)
        
        return
    
    def _CreateNewFENSwitchgear(self, config):
        # create a new switchgear device
        e = FENSwitchgearDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
        
        # create the device config
        deviceConfig = FENSwitchgearDevice.CreateFileConfigFromGridConfiguration(config)
        
        e.CreateNewFENSWitchgearFromFile(deviceConfig, self)
        
        return
    
    def _CreateNewConverter(self, config):
        # create a new converter device
        e = ConverterDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
        
        deviceConfig = ConverterDevice.CreateFileConfigFromGridConfiguration(config)
        
        e.CreateNewConverterFromFile(deviceConfig, self)
        
        return
    
    def _CreateNewSciBreakBreaker(self, config):
        # create a new breaker device
        e = SciBreakBreakerDevice(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
        
        deviceConfig = SciBreakBreakerDevice.CreateFileConfigFromGridConfiguration(config)
        
        e.CreateNewSciBreakBreakerFromFile(deviceConfig, self)
        
        return
    
    def _CreateNewSource(self, config):
        # create a new source device
        e = GridSource(self.editor, self.editorPage, self.networkInterface, self.scopeManager)
        
        sourceConfig = GridSource.CreateFileConfigFromGridConfiguration(config)
        
        e.CreateNewSourceFromFile(sourceConfig, self)