from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterDroopControlData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    voltage : int = field(default=0)
    droopParam : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterDroopControlData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterDroopControlData.")
        
        return struct.unpack(ConverterDroopControlData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        voltage, droopParam, _, __ = cls.ParseBytes(data)
        
        return ConverterDroopControlData(voltage, droopParam)