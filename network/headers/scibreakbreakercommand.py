from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.command import CommandHeader

class SciBreakBreakerCommand (IntEnum):
    # commands to control the breaker
    TURN_ON = int("0x0601", 16)
    TURN_OFF = int("0x0602", 16)
    OPEN = int("0x0201", 16)
    CLOSE = int("0x0202", 16)
    
    PERIODIC_DATA_ON = int("0x0401", 16)
    PERIODIC_DATA_OFF = int("0x0402", 16)
    
    SETTRIPLEVEL = int("0x0500", 16)

@dataclass
class SciBreakBreakerCommandHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.SCIBREAKBREAKER, init=False)
    command : int = field(default=0)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(headerBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(headerBytes)