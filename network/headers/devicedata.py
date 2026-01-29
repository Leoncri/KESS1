# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
import struct

from network.packetsegment import PacketSegment
from .header import Header, PacketType

@dataclass
class DeviceDataHeader(Header):
    """Header for packets with periodically send data.

    packetType is automatically set to DEVICEDATA.

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields (added):
        id (uint32): Upcounting number (see server documentation for details)
        rsvd (uint32): 
            is 0.
    
    TODO:
    - Description of rsvd
    """

    _typeFormatString = "II"
    fullTypeFormatString = Header.fullTypeFormatString + _typeFormatString
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    packetType : PacketType = field(default=PacketType.DEVICEDATA, init=False)
    id : int = field(default=0)
    rsvd : int = field(default=0, init=False)

    def GetBytes(self) -> bytearray:
        """Gives the bytearray representation of the DeviceDataHeader.

        The binary representation of the added fields are appended to the
        binary representation of Header.

        Returns:
            bytearray: Binary representation of all fields (even inherited
                ones).

        Raises:
            struct.error: The type of one of the added fields doesn't match
            with their stated ctype or the value is not in the expected range.
        """
        
        headerBytes = super().GetBytes()
        deviceDataHeaderBytes = struct.pack(DeviceDataHeader._typeFormatString,
            self.id, self.rsvd)
        return headerBytes + deviceDataHeaderBytes

    def ParseBytes(headerBytes: bytearray) -> tuple[int, int]:
        """ Retries deviceStatus, deviceErrors from a bytearray.

        Args:
            headerBytes (bytearray): Binary representation of added fields
                compared to header (id, rsvd). Only the
                bytes from 0 to size (exclusive) are considered. Further bytes
                don't have an effect.
        
        Returns:
            A tuple (id, rsvd)

        Raises:
            IndexError: Number of bytes in headerBytes is insufficient for
                creating a DeviceDataHeader.
        """
        if len(headerBytes) < DeviceDataHeader.size:
            raise IndexError("Error: Too few bytes for a DeviceDataHeader.")
        headerBytes = headerBytes[:DeviceDataHeader.size]
        deviceDataHeaderTuple = struct.unpack(
            DeviceDataHeader._typeFormatString, headerBytes)
        return deviceDataHeaderTuple