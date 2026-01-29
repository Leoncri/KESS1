from __future__ import annotations
from dataclasses import *
import struct

from network.payloads.gridelementconfigs import *
from network.payloads.gridelementconfigs.gridelementconfigparser import GridElementConfigParser

from .payload import Payload

@dataclass
class GridGetLengthRespondPayload(Payload):
    # payload for getting the number of grid config packets
    _typeFormatString = "IIII"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    numPackets : int = field(default=0)
    rsvd0 : int = field(default=0)
    rsvd1 : int = field(default=0)
    rsvd2 : int = field(default=0)
    
    def ParseBytes(getLengthPayloadBytes: bytearray) -> int:
        """Retrieves the number of packets.
        
        Args:
            getLengthPayloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
        
        Returns:
            The number of packets

        Raises:
            IndexError: Number of bytes in getLengthPayloadBytes is insufficient
                for creating an GridGetLengthRespondPayload.
        """
        if len(getLengthPayloadBytes) < GridGetLengthRespondPayload.totalSize:
            raise IndexError("Error: Too few bytes for an GetLengthHeader.")
        
        numPackets, _, __, ___ = struct.unpack(GridGetLengthRespondPayload._typeFormatString, getLengthPayloadBytes)
        return numPackets
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> GridGetLengthRespondPayload:
        """Creates an GridGetLengthRespondPayload based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
        
        Returns:
            GridGetLengthRespondPayload: The retrieved Payload.
            
        Raises:
            IndexError: Number of bytes in errorPayloadBytes is insufficient
                for creating an GridGetLengthRespondPayload.
        """
        numPackets = cls.ParseBytes(payloadBytes)
        return GridGetLengthRespondPayload(numPackets, 0,0,0)

class GridGetConfigRespondPayload(Payload):
    def __init__(self, gridElementConfigList : list[GridElementConfig]):
        self.gridElementConfigList = gridElementConfigList
    
    
    # payload for a grid config respond packet
    def ParseBytes(gridConfig : bytearray, length : int) -> list[GridElementConfig]:
        # call element parser
        return GridElementConfigParser.GetPayloadFromBytes(gridConfig, length)
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray, length: int) -> GridGetConfigRespondPayload:
        return GridGetConfigRespondPayload(cls.ParseBytes(payloadBytes, length))