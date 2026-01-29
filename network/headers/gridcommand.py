# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.command import CommandHeader

class GridCommand(IntEnum):
    """Specifies available commands for the grid.

    Values:
        CLEAR_ALL: Clear internal structure
        LOAD_GRID_CONFIG: Load grid topology file
        GET_GRID_CONFIG:
        SETUP_GRID:

    TODO:
    - Explaination of GET_GRID_CONFIG and SETUP_GRID
    """
    _base = int("0x1000", 16)
    _config = int("0x2000", 16)

    CLEAR_ALL = int("0x0001", 16) | _config,
    LOAD_GRID_CONFIG = int("0x0101", 16) | _config,
    GET_GRID_CONFIG = int("0x0102", 16) | _config,
    GET_CONFIG_LENGTH = int("0x0103", 16) | _config,
    
    SETUP_GRID = int("0x0201", 16) | _config

@dataclass
class GridCommandClearHeader(CommandHeader):
    # header for clearing the grid configuration
    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    command : int = field(default=GridCommand.CLEAR_ALL, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for the clear confiuration command
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class GridCommandSetupHeader(CommandHeader):
    # header for setting up the grid from a loaded config
    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    command : int = field(default=GridCommand.SETUP_GRID, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for the clear confiuration command
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class GridCommandGetLengthHeader(CommandHeader):
    # header for getting the number of grid config packets
    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    command : int = field(default=GridCommand.GET_CONFIG_LENGTH, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for getting the length
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class GridCommandGetConfigHeader(CommandHeader):
    # header for getting the grid config packets
    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    command : int = field(default=GridCommand.GET_GRID_CONFIG, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for getting the configuration
        return super().GetBytes()
    
    def ParseBytes(gridHeaderBytes :  bytearray):
        # returns the data inside the command header
        return super().ParseBytes(gridHeaderBytes)

@dataclass
class GridCommandLoadFileHeader(CommandHeader):
    """Header of a command to the server to load the grid from a file.

    packetType is automatically set to COMMAND, deviceType is set to GRID and
    command is set to LOAD_GRID_CONFIG.

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields (added):
        version (uint32): Version of PGS GridEditor. The default value 0.
        subversion (uint32): Subversion of PGS GridEditor. The default
            value is 0.
        totalParts (uint16): Total number of packets containing information
            about the grid. The default value is 0.
        part (uint16): Part number of this packet (e.g. 16 out of 20). For the
            first packet, part is 1 and for the last it is totalParts.
            The default value is 0.
        numberGridElements (uint32): Number of grid elements in the payload of
            the packet. The default value is 0.

    TODO:
    - allow multiple GridElements in one packet
    - specific documentation for GridCommand values
    """
    _typeFormatString = "IIHHI"
    fullTypeFormatString = (CommandHeader.fullTypeFormatString + 
        _typeFormatString)
    _typeFormatString = PacketSegment._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    deviceType : DeviceType = field(default=DeviceType.GRID, init=False)
    command : int = field(default=GridCommand.LOAD_GRID_CONFIG, init=False)
    
    version : int = field(default=0)
    subversion : int = field(default=0)
    totalParts : int = field(default=0)
    part : int = field(default=0)
    numberGridElements : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the GridCommandLoadGridFileHeader.

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
        commandHeaderBytes = super().GetBytes()
        gridHeaderBytes = struct.pack(GridCommandLoadFileHeader._typeFormatString,
            self.version, self.subversion, self.totalParts, self.part,
            self.numberGridElements)
        return commandHeaderBytes + gridHeaderBytes

    def ParseBytes(gridHeaderBytes: bytearray) -> tuple[int, int, int, int, int]:
        """Retrieves the added fields from a bytearray.

        Args:
            gridHeaderBytes (bytearray): Binary data of the added fields. Only
                the bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.

        Returns:
            A tuple representing (version, subversion, totalParts, part,
                numberGridElements)

        Raises:
            IndexError: Number of bytes in gridHeaderBytes is insufficient
                for creating GridCommandLoadFileHeader.
        """
        if len(gridHeaderBytes) < GridCommandLoadFileHeader.size:
            raise IndexError("Error: Too few bytes for a " /
                "GridCommandLoadFileHeader""")
        gridHeaderBytes = gridHeaderBytes[:GridCommandLoadFileHeader.size]
        loadGridFileTuple = struct.unpack(
            GridCommandLoadFileHeader._typeFormatString, gridHeaderBytes)
        return loadGridFileTuple