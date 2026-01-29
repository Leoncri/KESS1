from __future__ import annotations

from network.packets.packet import Packet
from network.headers.header import Header, DeviceType, PacketType
from network.payloads.error import ErrorPayload

class ErrorPacket(Packet):
    """Packet to describe errors.

    The packetType of the header is automatically ERROR.

    Attributes:
        header (Header): Uses Header (not derived classes) to state
            structural information (packetType, deviceType, deviceId, ...)
        payload (ErrorPayload): Details of the occured error

    TODO:
    - Testing ErrorPacket (including parsing)
    - add proper description for rsvd0

    """
    def __init__(self, header : Header, payload : ErrorPayload) -> ErrorPacket:
        """Creates an ErrorPacket based on already existing header and payload.

        Args:
            header (Header): Uses Header (not derived classes) to specify
                structural information.
            payload (ErrorPayload): Details of the occured error

        Returns:
            ErrorPacket: Packet, that was created by using existing header and
                payload.
        """
        super().__init__(header, payload)

    @classmethod
    def FromConfig(cls, deviceType : DeviceType, deviceId : int, error : int,
        rsvd : int) -> ErrorPacket:
        """Creates an ErrorPacket based on structural and status information.

        Args:
            deviceType (uint8): Describes the type of device, where the error
                occured. Accepts the in DeviceType specified values or their
                corresponding integers.
            deviceId (uint16): Identifier of the device, where the error
                occured.
            error (uint32): Describes the kind of error, which occured.
                Accepts the in ErrorType specified ErrorTypes, their
                corresponding integers values or any other integer in the
                uint32 range (ensure the server supports that type of error).
            rsvd0 (uint32): Reserved space for further information. See
                server for details.
        
        Returns:
            ErrorPacket: Packet, that was created by using structural and
                status information.

        Raises:
            struct.error: At least of one of the parameters doesn't correspond
                with their type or exceeds its range.
        """
        length = Header.totalSize + ErrorPayload.totalSize
        header = Header(PacketType.ERROR, deviceType, deviceId, length)
        payload = ErrorPayload(error, rsvd)

        return ErrorPacket(header, payload)