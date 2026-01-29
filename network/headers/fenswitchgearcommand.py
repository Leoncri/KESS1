from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.command import CommandHeader

class FENSwitchgearCommand(IntEnum):
    # commands for controlling a switchgear
    SET_SWITCH = int("0x0100", 16)
    RESET_SWITCH = int("0x0200", 16)
    GET_DATA = int("0x0300", 16)
    PERIODIC_DATA = int("0x0400", 16)
    
    PERIODIC_DATA_ON = int("0x0001", 16)
    PERIODIC_DATA_OFF = int("0x0002", 16)

@dataclass
class FENSwitchgearSwitchCommandHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.FENSWITCHGEAR, init=False)
    command : int = field(default=0)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class FENSwitchgearCommandPeriodicDataOnHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.FENSWITCHGEAR, init=False)
    command : int = field(default=(FENSwitchgearCommand.PERIODIC_DATA | FENSwitchgearCommand.PERIODIC_DATA_ON), init=False)
    
    def GetBytes(self):
        # return bytes of header
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class FENSwitchgearCommandPeriodicDataOffHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.FENSWITCHGEAR, init=False)
    command : int = field(default=(FENSwitchgearCommand.PERIODIC_DATA | FENSwitchgearCommand.PERIODIC_DATA_OFF), init=False)
    
    def GetBytes(self):
        # return bytes of header
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)