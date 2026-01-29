from enum import IntEnum
from network.packets.serverrespond import ServerStatusPacket
from network.packets.servercommand import *
from network.packetdistributor import *

class ServerStatus(IntEnum):
    GRID_LOADED = int("0x0001", 16)
    GRID_STARTED = int("0x0002", 16)
    
class ServerManager:
    def __init__(self, editor, networkInterface):
        # store paramters
        self.editor = editor
        self.networkInterface = networkInterface
        
        # packet distributor
        self.packetDistributor = PacketDistributor()
        
        # some data to store the server configuration
        self.gridLoaded = False
        self.gridStarted = False
        self.gridVersion = 0
        self.lastGridVersion = 0
        self.gridUpToDate = False
    
    def Reset(self):
        self.gridLoaded = False
        self.gridStarted = False
        self.gridVersion = 0
        self.lastGridVersion = 0
        self.gridUpToDate = False
        return
    
    def GetGridStatus(self):
        return self.gridUpToDate, self.gridLoaded, self.gridStarted
    
    def StartGrid(self):
        # check if grid is already started
        if self.gridStarted:
            return
        
        # create a StartGrid packet and send it so the network interface
        id, packet = ServerStartGridPacket.FromConfig()
        
        result = self._SendPacket(id, packet)
        if not result:
            return False
        
        return True
    
    def StopGrid(self):
        # create a StopGrid packet and send it to the server
        id, packet = ServerStopGridPacket.FromConfig()
        
        result = self._SendPacket(id, packet)
        if not result:
            return False
        
        return True
    
    def NewPacket(self, packet):
        # a new packet for the server manager
        if isinstance(packet, ServerStatusPacket):
            self._NewStatusPacket(packet)
        else:
            # notify packet distributor
            commandId = packet.header.commandId
            self.packetDistributor.NewPacketData(commandId, packet)
        return
    
    def _NewStatusPacket(self, statusPacket : ServerStatusPacket):
        # has something changed?
        changed = False
        
        # check if grid is loaded
        if (statusPacket.payload.status & ServerStatus.GRID_LOADED) != 0:
            gridLoaded = True
            
            # only check grid version when grid is already loaded
            if self.lastGridVersion != statusPacket.payload.fileVersion:               
                self.gridUpToDate = False
                changed = True
                self.lastGridVersion = statusPacket.payload.fileVersion
            
            # check if grid was recently loaded
            if self.editor.GridNotUpToDate():
                changed = True
                self.gridUpToDate = True
        
        else:
            gridLoaded = False
        
        # check if grid is started
        if (statusPacket.payload.status & ServerStatus.GRID_STARTED) != 0:
            gridStarted = True
            
        else:
            gridStarted = False
        
        if self.gridLoaded != gridLoaded or self.gridStarted != gridStarted:
            changed = True
        
        self.gridLoaded = gridLoaded
        self.gridStarted = gridStarted
        
        if changed:
            self.editor.ChangedServerStatus()
        
        return
    
    def _SendPacket(self, id, packet):
        # register packet, send data and wait for respond
        self.packetDistributor.RegisterTransfer(id)
        
        self.networkInterface.SendData(packet.GetBytes())
        
        return self.packetDistributor.WaitForTransferComplete(id)