# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
import struct

from network.packetsegment import PacketSegment
from .header import Header, PacketType

@dataclass
class CommandRespondHeader(Header):
    """Header of a respond by the server.

    packetType is automatically set to RESPOND.

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields (added):
        result (uint32): Result of the command. The default value is 0. When
            comparing result, won't be taken into account.
        commandId (uint32): Identifier of the command this packet is responding
            to. The default value is 0.
    """
    _typeFormatString = "II"
    fullTypeFormatString = Header.fullTypeFormatString + _typeFormatString
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    packetType : PacketType = field(default=PacketType.RESPOND, init=False)
    result : int = field(default=0, compare=False)
    commandId : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives a binary representation ofthe CommandRespondHeader.

        The binary form of the added fields is appended to the binary form
        of Header.

        Returns:
            bytearray: Binary representation of all fields (even inherited
                ones).

        Raises:
            struct.error: The type of one of the added fields doesn't match
                with _typeFormatString or the value is not in the specified
                range.
        """

        headerBytes = super().GetBytes()
        commandResponseBytes = struct.pack(
            CommandRespondHeader._typeFormatString, self.result,
            self.commandId)
        return headerBytes + commandResponseBytes

    def ParseBytes(headerBytes: bytearray) -> tuple[int, int]:
        """Retrieves result and commandId from a bytearray.

        Args:
            headerbytes (bytearray): Binary representation of the added
                fields. Only the bytes from 0 to size (exclusive) are
                considered. Further bytes don't have an effect.

        Returns:
            A tuple (result, commandId) describing the additional fields of
            CommandRespondHeader. 
        """
        if len(headerBytes) < CommandRespondHeader.size:
            raise IndexError("Error: Too few bytes for a CommandRespondHeader")
        commandRespondHeaderBytes = headerBytes[:CommandRespondHeader.size]
        commandResponseHeaderTuple = struct.unpack(
            CommandRespondHeader._typeFormatString, commandRespondHeaderBytes)
        return commandResponseHeaderTuple