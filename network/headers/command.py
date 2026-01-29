# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
import struct
import random

from network.packetsegment import PacketSegment
from .header import Header, PacketType

@dataclass
class CommandHeader(Header):
    """Header of a command send by GridEditor.

    packetType is automatically set to COMMAND.

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields (added):
        command (uint32): Command send by GridEditor to the Server. The default
            value is 0.
        commandId (uint32): Random identifier to distinguish multiple responses
            On default, the value will be generated automatically.
    """
    _typeFormatString = "II"
    fullTypeFormatString = Header.fullTypeFormatString + _typeFormatString
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    packetType: PacketType = field(default=PacketType.COMMAND, init=False)
    command : int = field(default=0)
    commandId : int = field(default=random.randint(0, 4294967295))

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the CommandHeader.

        The binary representation of the added fields are appended to the
        binary representation of Header.

        Returns:
            bytearray: Binary representation of all fields (even inherited
                ones).
        
        Raises:
            struct.error: The type of one of the added fields doesn't match
                with _typeFormatString or the value is not in the specified
                range.
        """
        headerBytes = super().GetBytes()
        commandBytes = struct.pack(CommandHeader._typeFormatString,
            self.command, self.commandId)
        return headerBytes + commandBytes

    def ParseBytes(headerBytes: bytearray) -> tuple[int, int]:
        """Retrieves command and commandId from a bytearray.

        Args:
            headerBytes (bytearray): Binary data of the added fields.
                Only the bytes from 0 to size (exclusive) are considered.
                Further bytes don't have an effect.

        Returns:
            A tuple representing (command, commandId)

        Raises:
            IndexError: Number of bytes in headerBytes is insufficient for
                creating CommandHeader
        """
        if len(headerBytes) < CommandHeader.size:
            raise IndexError("Error: Too few bytes for a CommandHeader.")
        commandHeaderBytes = headerBytes[:CommandHeader.size]
        commandHeaderTuple = struct.unpack(CommandHeader._typeFormatString,
            commandHeaderBytes)
        return commandHeaderTuple