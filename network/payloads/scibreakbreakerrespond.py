from __future__ import annotations
from dataclasses import *
import struct
from enum import IntEnum

from .payload import Payload

class SciBreakBreakerStatus(IntEnum):
    # commands for controlling a switchgear
    ONLINE = int("0x01", 16)
    CLOSED_TOP = int("0x02", 16)
    CLOSED_BOT = int("0x04", 16)
    FAULT = int("0x04", 16)
    TRIP = int("0x08", 16)

@dataclass
class SciBreakBreakerLiveDataPayload(Payload):
    # payload for scibreak breaker live data
    _typeFormatString = "Ihhhhhh"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    status : int = field(default=0)
    voltageTop : int = field(default=0)
    voltageBot : int = field(default=0)
    currentTop : int = field(default=0)
    currentBot : int = field(default=0)
    tripLevelTop : int = field(default=0)
    tripLevelBot : int = field(default=0)
    
    def ParseBytes(payloadBytes :  bytearray):
        # parse the bytes into switchgear data
        if len(payloadBytes) != SciBreakBreakerLiveDataPayload.totalSize:
            raise IndexError("Error: Number of bytes does not match length of SciBreakBreakerLiveDataPayload.")
        
        # split the struct
        status, voltageTop, voltageBot, currentTop, currentBot, tripLevelTop, tripLevelBot = struct.unpack(SciBreakBreakerLiveDataPayload._typeFormatString, payloadBytes)
        return (status, voltageTop, voltageBot, currentTop, currentBot, tripLevelTop, tripLevelBot)
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> SciBreakBreakerLiveDataPayload:
        # split bytes and create a new class
        status, voltageTop, voltageBot, currentTop, currentBot, tripLevelTop, tripLevelBot = cls.ParseBytes(payloadBytes)
        
        return SciBreakBreakerLiveDataPayload(status, voltageTop, voltageBot, currentTop, currentBot, tripLevelTop, tripLevelBot)