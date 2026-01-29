from __future__ import annotations
import random

from network.packets.packet import Packet
from network.headers.fenswitchgearcommand import *

class FENSwitchgearSetSwitchPacket(Packet):
    # packet for setting switches in a switchgear
    def __init__(self, header : FENSwitchgearSwitchCommandHeader) -> FENSwitchgearSetSwitchPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId, switches) -> tuple[int, FENSwitchgearSetSwitchPacket]:
        # create a new packet from a given config
        length = FENSwitchgearSwitchCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = FENSwitchgearSwitchCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = FENSwitchgearCommand.SET_SWITCH | switches)
        
        return commandId , FENSwitchgearSetSwitchPacket(commandHeader)

class FENSwitchgearResetSwitchPacket(Packet):
    # packet for resetting switches in a switchgear
    def __init__(self, header : FENSwitchgearSwitchCommandHeader) -> FENSwitchgearResetSwitchPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId, switches) -> tuple[int, FENSwitchgearResetSwitchPacket]:
        # create a new packet from a given config
        length = FENSwitchgearSwitchCommandHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = FENSwitchgearSwitchCommandHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId,
            command    = FENSwitchgearCommand.RESET_SWITCH | switches)
        
        return commandId , FENSwitchgearResetSwitchPacket(commandHeader)

class FENSwitchgearLiveDataOnPacket(Packet):
    # packet for receiving the live data from this device
    def __init__(self, header : FENSwitchgearCommandPeriodicDataOnHeader) -> FENSwitchgearLiveDataOnPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, FENSwitchgearLiveDataOnPacket]:
        # create a new packet from a given config
        length = FENSwitchgearCommandPeriodicDataOnHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = FENSwitchgearCommandPeriodicDataOnHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, FENSwitchgearLiveDataOnPacket(commandHeader)

class FENSwitchgearLiveDataOffPacket(Packet):
    # packet for receiving the live data from this device
    def __init__(self, header : FENSwitchgearCommandPeriodicDataOffHeader) -> FENSwitchgearLiveDataOffPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # get the bytes of a packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls, deviceId) -> tuple[int, FENSwitchgearLiveDataOffPacket]:
        # create a new packet from a given config
        length = FENSwitchgearCommandPeriodicDataOffHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        # create header
        commandHeader = FENSwitchgearCommandPeriodicDataOffHeader(
            deviceId    = deviceId,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, FENSwitchgearLiveDataOffPacket(commandHeader)