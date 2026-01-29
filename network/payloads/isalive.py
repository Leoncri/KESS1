from __future__ import annotations
from dataclasses import *
import struct

from .payload import Payload

@dataclass
class IsAlivePayload(Payload):
    """Payload to describe the connection is still alive.
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        rsvd0 (uint32): Reserved field. For details see server
            documentation. The default is 0 (mostly used).
        rsvd1 (uint32): Reserved field. For details see server
            documentation. The default is 0 (mostly used).
    """
    _typeFormatString = "II"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct. calcsize(fullTypeFormatString)

    rsvd0 : int = field(default=0)
    rsvd1 : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the IsAlivePayload.
        
        Returns:
            bytearray: Binary representation of the fields.
            
        Raises:
            struct.error: The type of one of the fields doesn't match with
                _typeFormatString or the values are not within the expected
                range.
        """
        return struct.pack(IsAlivePayload._typeFormatString, self.rsvd0, self.rsvd1)

    def ParseBytes(isAliveBytes: bytearray) -> tuple[int, int]:
        """Retrieves rsvd0 and rsvd1 from binary data.
        
        Args:
            errorPayloadBytes (bytearray): rsvd0 and rsvd1 in binary form.
                Only bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (rsvd0, resvd1)
            
        Raises:
            IndexError: Number of bytes in isAliveBytes is insufficient
                for creating an IsAlivePayload.
        """
        if len(isAliveBytes) < IsAlivePayload.totalSize:
            raise IndexError("Error: Too Few bytes for an IsAlivePayload.")
        isAliveTuple = struct.unpack(IsAlivePayload._typeFormatString,
            isAliveBytes)
        return isAliveTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> Payload:

        (rsvd0, rsvd1) = cls.ParseBytes(payloadBytes)
        return IsAlivePayload(rsvd0, rsvd1)