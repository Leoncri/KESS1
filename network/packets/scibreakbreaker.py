from __future__ import annotations
import random

from network.packets.packet import Packet
from network.headers.scibreakbreakercommand import *
from network.payloads.scibreakbreaker import *

class SciBreakBreakerSetTripLevelPacket(Packet):
    # packet for setting the trip level
    def __init__(self, header : SciBreakBreakerCommandHeader, payload : SciBreakBreakerTripLevelPayload):
        self.header = header
        self.payload = payload
    
    def GetBytes(self):
        packetBytes = self.header.GetBytes() + self.payload.GetBytes()
        
        return self.AddPadding(packetBytes)
    
    @classmethod
    def FromConfig(cls, deviceId, data : list[int]) -> tuple[int, SciBreakBreakerSetTripLevelPacket]:
        # create a new packet from a given config
        headerLength = SciBreakBreakerCommandHeader.totalSize
        payloadLength = SciBreakBreakerTripLevelPayload.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = headerLength + payloadLength,
            connection  = 0,
            commandId   = commandId,
            command     = SciBreakBreakerCommand.SETTRIPLEVEL)
        
        payload = SciBreakBreakerTripLevelPayload(data)
        
        return commandId, SciBreakBreakerSetTripLevelPacket(commandHeader, payload)

class SciBreakBreakerTurnOnPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, SciBreakBreakerTurnOnPacket]:
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.TURN_ON)
        
        return commandId , SciBreakBreakerTurnOnPacket(commandHeader)

class SciBreakBreakerTurnOffPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, SciBreakBreakerTurnOffPacket]:
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.TURN_OFF)
        
        return commandId , SciBreakBreakerTurnOffPacket(commandHeader)

class SciBreakBreakerOpenPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, SciBreakBreakerOpenPacket]:
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.OPEN)
        
        return commandId , SciBreakBreakerOpenPacket(commandHeader)

class SciBreakBreakerClosePacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId):
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.CLOSE)
        
        return commandId , SciBreakBreakerClosePacket(commandHeader)

class SciBreakBreakerLiveDataOnPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId):
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.PERIODIC_DATA_ON)
        
        return commandId , SciBreakBreakerLiveDataOnPacket(commandHeader)

class SciBreakBreakerLiveDataOffPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : SciBreakBreakerCommandHeader):
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId):
        # create a new packet from a given config
        length = SciBreakBreakerCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = SciBreakBreakerCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = SciBreakBreakerCommand.PERIODIC_DATA_OFF)
        
        return commandId , SciBreakBreakerLiveDataOffPacket(commandHeader)