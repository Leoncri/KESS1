# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment

class PacketType(IntEnum):
    """Specifies the type of packet.

    Values:
        ISALIVE: IsAlive Packet
        COMMAND: Packet with CommandHeader
        RESPOND: Packet with CommandRespondHeader
        ERROR: Error Packet
        DEVICEDATA: Packet with a DeviceDataHeader

    TODO:
    - Validate upper explaination ("specifies ... ")
    """
    ISALIVE = int("0x00", 16),
    COMMAND = int("0x01", 16),
    RESPOND = int("0x81", 16),
    ERROR = int("0x82", 16)
    DEVICEDATA = int("0x11", 16)

class DeviceType(IntEnum):
    """Specifies type of device the packet is about.

    Values:
        NONE: None of the categories below fit. Especially IsAlive and Error
            packets have this device type.
        SERVER: Not an actual device, but used for simple responses send by
            the server.
        GRID: Not an actual device, but information about the grid. Might
            contain multiple grid types (e.g. nodes, points, segments,
            converters, breakers, switchgears).
        CONVERTER: Information about a single converter
        BREAKER: Information about a single breaker
        FENSWITCHGEAR: Information about a single FEN switchgear
    """
    NONE = int("0x0", 16),
    SERVER = int("0x01", 16),
    GRID = int("0x02", 16),
    SOURCE = int("0x11", 16),
    CONVERTER = int("0x41", 16),
    BREAKER = int("0x42", 16),
    FENSWITCHGEAR = int("0xC1", 16)
    SCIBREAKBREAKER = int("0xC2", 16)

@dataclass
class Header(PacketSegment):
    """Base class of every header.

    Some packets use this base class directly (e.g. ErrorPacket).

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        packetType (uint8): Describes the type of packet. Accepts the in
            PacketType named values or their corresponding integers. The
            default value is COMMAND.
        deviceType (uint8): Describes the type of device the packet is about.
            Accepts the in DeviceType named values or their corresponding
            integers. The default value is NONE.
        deviceId (uint16): Identifier of the device. The default value is 0.
        length (uint16): Total length in bytes of the packet. The default
            value is 0.
        connection (uint16): Identifier given by the server to distinguish
            between multiple connection. There is no purpose on the GridEditor
            site. The default value is 0. When comparing connection won't be
            taken into account.
    """

    _typeFormatString = PacketSegment._byteOrder + "BBHHH"
    fullTypeFormatString = _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    packetType: PacketType = field(default=PacketType.COMMAND)
    deviceType : DeviceType = field(default=DeviceType.NONE)
    deviceId : int = field(default=0)
    length : int = field(default=0)
    connection : int = field(default=0, compare=False)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the Header.

        Returns:
            bytearray: Binary representation of all fields

        Raises:
            struct.error: The type of one of the fields doesn't match with
                _typeFormatString or the values are not within the expected
                range.
        """
        return struct.pack(Header._typeFormatString, self.packetType,
            self.deviceType, self.deviceId, self.length, self.connection)

    def ParseBytes(headerBytes: bytearray) -> tuple[PacketType,
        DeviceType, int, int]:
        """Retrieves the fields from a bytearray.

        Args:
            headerBytes (bytearray): Binary data of the fields. Only the bytes
                from 0 to size (exclusive) are considered. Further bytes don't
                have an effect.
        
        Returns:
            A tuple representing (packetType, deviceType, deviceId, length,
            connection)

        Raises:
            IndexError: Number of bytes in headerBytes is insufficient for
                creating a Header.
        """
        if len(headerBytes) < Header.size:
            raise IndexError("Error: Too few bytes for a Header.")
        headerBytes = headerBytes[:Header.size]
        (packetType, deviceType, deviceId, length, connection) = struct.unpack(
            Header.fullTypeFormatString, headerBytes)
        return (packetType, deviceType, deviceId, length, connection)