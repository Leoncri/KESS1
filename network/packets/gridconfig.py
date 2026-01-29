from __future__ import annotations
import random
from math import ceil

from network.packets.packet import Packet
from network.headers.gridcommand import GridCommandLoadFileHeader
from network.headers.gridcommand import GridCommandClearHeader
from network.headers.gridcommand import GridCommandSetupHeader
from network.headers.gridcommand import GridCommandGetLengthHeader
from network.headers.gridcommand import GridCommandGetConfigHeader
from network.payloads.gridelementconfigs import *
from auxillary.versioninfo import VersionInfo

class GridClearPacket(Packet):
# packet clearing the grid
    def __init__(self, header : GridCommandClearHeader) -> GridClearPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls) -> tuple[int, GridClearPacket]:
        # create a packet from preset config
        length = GridCommandClearHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = GridCommandClearHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, GridClearPacket(commandHeader)

class GridSetupPacket(Packet):
# packet for setting up the uploaded grid
    def __init__(self, header : GridCommandSetupHeader) -> GridSetupPacket:
        self.header = header
    
    def GetBytes(self) -> bytearray:
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls) -> tuple[int, GridSetupPacket]:
        # create a packet from preset config
        length = GridCommandClearHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = GridCommandSetupHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, GridSetupPacket(commandHeader)

class GridGetConfigSizePacket(Packet):
    # packet for getting the number of grid config packets
    def __init__(self, header : GridCommandGetLengthHeader) -> GridGetConfigSizePacket:
        self.header = header;
    
    def GetBytes(self) -> bytearray:
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls) -> tuple[int, GridGetConfigSizePacket]:
        # create a packet from preset config
        length = GridCommandGetLengthHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = GridCommandGetLengthHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, GridGetConfigSizePacket(commandHeader)

class GridGetConfigPacket(Packet):
    # packet for getting the actual grid configuration
    def __init__(self, header : GridCommandGetConfigHeader) -> GridGetConfigPacket:
        self.header = header;
    
    def GetBytes(self) -> bytearray:
        # returns the bytes of the packet
        return self.header.GetBytes()
    
    @classmethod
    def FromConfig(cls) -> tuple[int, GridGetConfigPacket]:
        # create a packet from preset config
        length = GridCommandGetConfigHeader.totalSize
        commandId = random.randint(0, 2 ** 32 - 1)
        
        commandHeader = GridCommandGetConfigHeader(
            deviceId    = 0,
            length      = length,
            connection  = 0,
            commandId   = commandId)
        
        return commandId, GridGetConfigPacket(commandHeader)

class GridConfigPacket(Packet):
    """Packet describing (a part of) the grid file.
    
    Attributes:
        header (GridCommandLoadFileHeader): Header of the packet
        payload (List[GridElementConfig or derived class]): GridElementConfigs,
            which shall be in the packet. 
    """
    def __init__(self, header : GridCommandLoadFileHeader,
        payload : list[GridElementConfig]) -> GridConfigPacket:
        """Creates a GridConfigPacket based on an existing header and an
        existing payload.

        Args:
            header (GridCommandLoadFileHeader): General and structural
                information
            payload (list(GridElementConfig)): List of GridElementConfigs
        """
        self.header = header
        self.payload = payload

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the GridConfigPacket.
        
        All packets have a length of multiples of 16. If required, the end
        will be filled up with zero bytes.
        
        Return:
            bytearray: Binary representation of header and payload (in
                that order).
        """
        headerBytes = self.header.GetBytes()
        payloadBytesList = []

        for payload in self.payload:
            payloadBytesList.append(
                payload.GetBytes()
            )
        # merge bytearrays of single GridElementConfigs into one bytearray
        payloadBytes = b''.join(payloadBytesList)
        unpadded =headerBytes + payloadBytes
        return self.AddPadding(unpadded)

    @classmethod
    def FromConfig(cls, gridElements : list[GridElementConfig],
        versionInfo: VersionInfo) -> tuple[int, list[GridConfigPacket]]:
        """Creates a list of GridConfigPacket based on structural (header) and the
        GridElementConfigs (actual payload).

        The gridElements are splitted in multiple packets, if the length of a
        single packet would exceed the maximum size. deviceId is set to 0.
        Connection is 0 as well.
        
        Args:
            gridElements (list(GridElementConfig)): GridElementConfigs, which
                shall be send in this packet
            versionInfo (VersionInfo): Stores version (uint32) and
                subversion (uint32) of the GridEditor.
        
        Returns:
            list[GridConfigPacket]: Packets, that was created by using structural
                information (header) and information about the
                GridElementConfigs. part of the first packet is 1 and
                totalParts for the last.
        """
        headerLength = GridCommandLoadFileHeader.totalSize
        totalNumberGridElements = len(gridElements)
        maxElementsPerPacket = cls._CalcMaxElementsPerPacket()
        packets = []

        deviceId = 0
        # connection will be set by the server
        connection = 0
        # id to distinguish between different command packets
        commandId = random.randint(0, 2 ** 32 - 1)
        totalParts = cls._CalcNumberPackets(totalNumberGridElements)
        
        for part in range(1, totalParts + 1):
            sliceStart = (part - 1) * maxElementsPerPacket
            sliceEnd = part * maxElementsPerPacket
            payload = gridElements[sliceStart : sliceEnd]
            numberGridElements = len(payload)
            payloadLength = GridElementConfig.maxTotalSize * numberGridElements
            length = headerLength + payloadLength
            
            header = GridCommandLoadFileHeader(deviceId=deviceId, length=length,
                connection=connection, commandId=commandId,
                version=versionInfo.version, subversion=versionInfo.subversion,
                totalParts=totalParts, part=part,
                numberGridElements=numberGridElements)
            packets.append(GridConfigPacket(header, payload))

        return (commandId, packets)
    @classmethod
    def _CalcMaxElementsPerPacket(cls) -> int:
        """Returns:
            Maximum number of grid elements, which fit into a single
            packet.
        """
        headerSize = GridCommandLoadFileHeader.totalSize
        payloadSize = GridElementConfig.maxTotalSize
        maxElementsPerPacket = (cls.maxSizePacket - headerSize) // payloadSize
        return maxElementsPerPacket

    @classmethod
    def _CalcNumberPackets(cls, numberGridElements : int) -> int:
        """Determines the required number of packets for a given number of
        grid elements.
        
        Args:
            numberGridElements (int): Number of grid elements
        
        Returns:
            An integer stating the required number of packets.
        """
        maxElementsPerPacket = cls._CalcMaxElementsPerPacket()
        numberPackets = ceil(numberGridElements / maxElementsPerPacket)
        return numberPackets
