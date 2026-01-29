from __future__ import annotations
import random

from network.packets.packet import Packet
from network.headers.convertercommand import *
from network.payloads.converter import *

class ConverterSetModePacket(Packet):
    # packet for setting a specific mode
    def __init__(self, header : ConverterCommandSetModeHeader) -> ConverterSetModePacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId, mode) -> tuple[int, ConverterSetModePacket]:
        # create a new packet from a given config
        length = ConverterCommandSetModeHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ConverterCommandSetModeHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command     = ConverterCommand.SET_MODE | mode)
        
        return commandId, ConverterSetModePacket(commandHeader)

class ConverterUpdateDataPacket(Packet):
    # packte for updating a specific part of the converter parameter list
    def __init__(self, header : ConverterCommandUpdateDataHeader, payload : ConverterUpdateDataPayload) -> ConverterUpdateDataPacket:
        self.header = header
        self.payload = payload
    
    def GetBytes(self) -> bytearray:
        # return the bytes of the packet
        packetBytes = self.header.GetBytes() + self.payload.GetBytes()
        
        return self.AddPadding(packetBytes)
    
    @classmethod
    def FromConfig(cls, deviceId, mode, data : list[int]) -> tuple[int, ConverterUpdateDataPacket]:
        # create a new packet from a given config
        headerLength = ConverterCommandUpdateDataHeader.totalSize
        payloadLength = ConverterUpdateDataPayload.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ConverterCommandUpdateDataHeader(
            deviceId    = deviceId,
            length      = headerLength + payloadLength,
            connection  = 0,
            commandId   = commandId,
            command     = ConverterCommand.UPDATE_DATA | mode)
        
        payload = ConverterUpdateDataPayload(data)
        
        return commandId, ConverterUpdateDataPacket(commandHeader, payload)

class ConverterLiveDataOnPacket(Packet):
    # packet for turning the live data on
    def __init__(self, header : ConverterCommandPeriodicDataOnHeader) -> ConverterLiveDataOnPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, ConverterLiveDataOnPacket]:
        # create a new packet from config
        length = ConverterCommandPeriodicDataOnHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ConverterCommandPeriodicDataOnHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, ConverterLiveDataOnPacket(commandHeader)

class ConverterLiveDataOffPacket(Packet):
    # packet for turning the live data on
    def __init__(self, header : ConverterCommandPeriodicDataOffHeader) -> ConverterLiveDataOffPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, ConverterLiveDataOffPacket]:
        # create a new packet from config
        length = ConverterCommandPeriodicDataOffHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = ConverterCommandPeriodicDataOffHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, ConverterLiveDataOffPacket(commandHeader)