from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterVoltageControlData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    voltage : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterVoltageControlData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterVoltageControlData.")
        
        return struct.unpack(ConverterVoltageControlData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        voltage, _, __, ___ = cls.ParseBytes(data)
        
        return ConverterVoltageControlData(voltage)