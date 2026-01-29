from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterStaticData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    modes : int = field(default=0)
    power : float = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterStaticData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterStaticData.")
        
        return struct.unpack(ConverterStaticData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        modes, p, _, __ = cls.ParseBytes(data)
        
        # calculate actual power
        sig = (p & 0xFFC0) >> 6
        exp = (p & 0x003F)
        
        power = sig * 10**exp
        
        return ConverterStaticData(modes, power)