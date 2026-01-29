from __future__ import annotations
import random

from network.packets.packet import Packet
from network.headers.servercommand import *

class ServerStartGridPacket(Packet):
    # packet for starting the grid
    def __init__(self, header : ServerCommandStartGridHeader) -> ServerStartGridPacket:
        self.header = header
    
    def GetBytes(self):
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls):
        length = ServerCommandStartGridHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ServerCommandStartGridHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, ServerStartGridPacket(commandHeader)

class ServerStopGridPacket(Packet):
    # packet for stopping the grid
    def __init__(self, header : ServerCommandStopGridHeader) -> ServerStopGridPacket:
        self.header = header
    
    def GetBytes(self):
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls):
        length = ServerCommandStopGridHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ServerCommandStopGridHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, ServerStopGridPacket(commandHeader)