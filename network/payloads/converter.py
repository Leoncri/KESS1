from __future__ import annotations
from dataclasses import *
import struct

from .payload import Payload

@dataclass
class ConverterUpdateDataPayload(Payload):
    # payload for converter parameters
    _typeFormatString = "HHHHII"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    data : List = field(default=lambda: [])
    
    def GetBytes(self) -> bytearray:
        # return the bytes of the packet
        dataBytes = struct.pack(ConverterUpdateDataPayload._typeFormatString, *self.data, 0, 0)
        return dataBytes
    
    def ParseBytes(payloadBytes : bytearray) -> list[int]:
        # parse the bytes into switchgear data
        if len(payloadBytes) != ConverterUpdateDataPayload.totalSize:
            raise IndexError("Error: Number of bytes does not match length of ConverterUpdateDataPayload.")
        
        # split the struct
        d1, d2, d3, d4, _, __ = struct.unpack(ConverterUpdateDataPayload._typeFormatString, payloadBytes)
        return [d1, d2, d3, d4]
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> ConverterUpdateDataPayload:
        # split bytes and create a new class
        d1, d2, d3, d4, _, __ = cls.ParseBytes(payloadBytes)
        
        return ConverterUpdateDataPayload([d1, d2, d3, d4])