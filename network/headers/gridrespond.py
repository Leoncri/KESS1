# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.commandrespond import CommandRespondHeader

class GridRespond(IntEnum):
    """Specifies available respond types for grid commands.

    Values:
        SUCCESS: Command was successfully executed
        FAILURE: Tried executing command, but failed.
        UNKOWN_COMMAND: Received command is unkown to the server.
        BUFFER_SIZE: The buffer of the server is full. Retry sending packet
            later.
        NOT_READY:
        SETUP_ERROR:

    TODO:
    - fill explaination for NOT_READY, SETUP_ERROR
    """
    SUCCESS = int("0x0001", 16),
    GET_CONFIG_DATA = int("0x0002", 16),
    GET_CONFIG_LENGTH = int("0x0003", 16),
    FAILURE = int("0x0100", 16),
    UNKOWN_COMMAND = int("0x0101", 16),
    BUFFER_SIZE = int("0x0102", 16),
    NOT_READY = int("0x0103", 16),
    SETUP_ERROR = int("0x0104", 16),
    GET_CONFIG_ERROR = int("0x0105", 16)

@dataclass
class GridCommandGetFileHeader(CommandRespondHeader):
    """Header of a command to get the grid file.

    packetType is automatically set to RESPOND, deviceType is set to GRID.

    length stores the number of bytes used by the header and by the payload
    (numberGridElements * GridElementConfig.maxTotalSize).

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields (added):
        version (uint32): Version of PGS GridEditor. The default value
            is 0.
        subversion (uint32): Subversion of PGS GridEditor. The default value
            is 0.
        totalParts (uint16): Total number of packets containing information
            about the grid. The default value is 0.
        part (uint16): Part number of this packet (e.g. 16 out of 20). For the
            first packet, part is 1 and for the last it is totalParts.
            The default value is 0.
        numberGridElements(uint32): Number of grid elements in the payload of
            the packet. The default value is 0.
    """
    _typeFormatString = "IIHHI"
    fullTypeFormatString = CommandRespondHeader.fullTypeFormatString + _typeFormatString
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    
    version : int = field(default=0)
    subversion : int = field(default=0)
    totalParts : int = field(default=0)
    part : int = field(default=0)
    numberGridElements : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the GridCommandGetFileHeader.

        The binary representation of the added fields are appended to the
        binary representation of CommandHeader.

        Returns:
            bytearray: Binary representation of all fields (even inherited
                ones)

        Raises:
            struct.error: The type of one of the added fields doesn't match
                with _typeFormatString or the value is not within the specified
                range.
        """
        commandRespondHeaderBytes = super().GetBytes()
        getFileHeaderBytes = struct.pack(
            GridCommandGetFileHeader._typeFormatString,
            self.version, self.subversion, self.totalParts, self.part,
            self.numberGridElements)
        return commandRespondHeaderBytes + getFileHeaderBytes

    def ParseBytes(getFileHeaderBytes: bytearray) -> tuple[int, int, int, int, int]:
        """Retrieves the added fields from a bytearray.

        Args:
            gridHeaderBytes: Binary data of the added fields. Only the bytes
                from 0 to size (exclusive) are considered. Furhter bytes don't
                have an effect.

        Returns:
            A tuple representing (version, subversion, totalParts, part,
                numberGridElements)
        """
        if len(getFileHeaderBytes) < GridCommandGetFileHeader.size:
            raise IndexError("Error: Too few bytes for a " / 
                "GridCommandGetFileHeader")
        getFileHeaderBytes = getFileHeaderBytes[:GridCommandGetFileHeader.size]
        getFileHeaderTuple = struct.unpack(
            GridCommandGetFileHeader._typeFormatString, getFileHeaderBytes)
        return getFileHeaderTuple        