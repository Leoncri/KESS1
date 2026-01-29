from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

@dataclass
class ConverterVoltageData:
    _typeFormatString = "HHHH"
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    
    voltageP1 : int = field(default=0)
    voltageM1 : int = field(default=0)
    voltageP2 : int = field(default=0)
    voltageM2 : int = field(default=0)

    def ParseBytes(data : bytearray) -> tuple[int, int, int, int]:
        # chekc length and return data
        if len(data) != ConverterVoltageData.size:
            raise IndexError("Error: Number of bytes does not match length of ConverterVoltageData.")
        
        return struct.unpack(ConverterVoltageData._typeFormatString, data)

    @classmethod
    def GetDataFromBytes(cls, data : bytearray):
        vp1, vm1, vp2, vm2 = cls.ParseBytes(data)
        
        return ConverterVoltageData(vp1, vm1, vp2, vm2)