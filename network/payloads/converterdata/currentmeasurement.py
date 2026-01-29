from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterCurrentData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    currentP1 : int = field(default=0)
    currentM1 : int = field(default=0)
    currentP2 : int = field(default=0)
    currentM2 : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterCurrentData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterCurrentData.")
        
        return struct.unpack(ConverterCurrentData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        vp1, vm1, vp2, vm2 = cls.ParseBytes(data)
        
        vp1 -= 0x8000
        vm1 -= 0x8000
        vp2 -= 0x8000
        vm2 -= 0x8000
        
        return ConverterCurrentData(vp1, vm1, vp2, vm2)