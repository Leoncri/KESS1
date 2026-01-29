from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterPrechargeData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    nextMode : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterPrechargeData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterPrechargeData.")
        
        return struct.unpack(ConverterPrechargeData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        nextMode, _, __, ___ = cls.ParseBytes(data)
        
        return ConverterPrechargeData(nextMode)