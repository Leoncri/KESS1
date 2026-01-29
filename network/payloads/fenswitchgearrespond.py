from __future__ import annotations
from dataclasses import *
import struct
from enum import IntEnum

from .payload import Payload

class FENSwitchgearStatus(IntEnum):
    # commands for controlling a switchgear
    ONLINE = int("0x01", 16)

@dataclass
class FENSwitchgearLiveDataPayload(Payload):
    # payload for switchgear live data
    _typeFormatString = "BBBBHHHHHH"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    closedSwitches  : int = field(default=0)
    lockedSwitches  : int = field(default=0)
    hvOnLine        : int = field(default=0)
    deviceStatus    : int = field(default=0)
    voltageP : int = field(default=0)
    voltageM : int = field(default=0)
    current1 : int = field(default=0)
    current2 : int = field(default=0)
    current3 : int = field(default=0)
    current4 : int = field(default=0)
    
    def ParseBytes(payloadBytes :  bytearray) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        # parse the bytes into switchgear data
        if len(payloadBytes) != FENSwitchgearLiveDataPayload.totalSize:
            raise IndexError("Error: Number of bytes does not match length of FENSwitchgearLiveDataPayload.")
        
        # split the struct
        closed, locked, hv, status, vp, vm, c1, c2, c3, c4 = struct.unpack(FENSwitchgearLiveDataPayload._typeFormatString, payloadBytes)
        return (closed, locked, hv, status, vp, vm, c1, c2, c3, c4)
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> FENSwitchgearLiveDataPayload:
        # split bytes and create a new class
        closed, locked, hv, status, vp, vm, c1, c2, c3, c4 = cls.ParseBytes(payloadBytes)
        
        return FENSwitchgearLiveDataPayload(closedSwitches=closed, lockedSwitches=locked,
                                            hvOnLine=hv, deviceStatus=status, voltageP=vp,
                                            voltageM=vm, current1=c1, current2=c2,
                                            current3=c3, current4=c4)