from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterPowerControlData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    power : float = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterPowerControlData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterPowerControlData.")
        
        return struct.unpack(ConverterPowerControlData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        power, _, __, ___ = cls.ParseBytes(data)
        
        power -= 0x8000
        power /= 100
        
        return ConverterPowerControlData(power)