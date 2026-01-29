from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterStatusData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    state : int = field(default=0)
    warnings : int = field(default=0)
    errors : int = field(default=0)
    mode : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterStatusData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterStatusData.")
        
        return struct.unpack(ConverterStatusData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        status, warnings, errors, mode = cls.ParseBytes(data)
        
        return ConverterStatusData(status, warnings, errors, mode)