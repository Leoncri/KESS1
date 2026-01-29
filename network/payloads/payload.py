from __future__ import annotations
from dataclasses import *

from network.packetsegment import PacketSegment

@dataclass
class Payload(PacketSegment):
    """Used as a base class for more specific payloads only.

    Attributes:
        _typeFormatString (string): Format string of additional fields; empty
        fullTypeFormatString (string): Format string of all fields; contains
            byte order symbol
    """
    _typeFormatString = ""
    fullTypeFormatString = PacketSegment._byteOrder
    
    def ParseBytes(payloadBytes : bytearray) -> None:
        """Used by derived classes to parse the fields from binary data.
        
        Returns:
            A tuple of the retrieved fields.
            
        Raises:
            IndexError: Number of bytes in payloadBytes is insufficient for
                creating the payload."""
        pass

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> Payload:
        """Used by derived classes to create a payload from binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            The retrieved payload.
        
        Raises:
            IndexError: Number of bytes in errorPayloadBytes is insufficient
                for creating an ErrorPayload."""
        pass

