from __future__ import annotations

from network.packets.packet import Packet
from network.headers.header import Header, PacketType, DeviceType
from network.payloads.isalive import IsAlivePayload

class IsAlivePacket(Packet):
    """Packet to confirm the connection is still open.

    Attributes:
        header (Header): Header (not derived class) is used to provide
            structural information (e.g. packetType, deviceType, deviceId, ...)
        payload (IsAlivePayload): Provides reserved fields for further
            information (see server for details)
    """
    def __init__(self, header: Header, payload : IsAlivePayload) -> None:
        """Creates an IsAlivePacket based on an existing header and an existing
        payload.

        Args:
            header (Header): Header (not derived class) is used to provide
                structural information (e.g. packetType, deviceType,
                deviceId, ...)
            payload (IsAlivePayload): Provides reserved fields for further
                information (see server for details)
        Return:
            IsAlivePacket: Packet based on an existing header and an existing
                payload.
        """
        super().__init__(header, payload)

    @classmethod
    def FromConfig(cls, rsvd0 : int = 0, rsvd1 : int = 0) -> IsAlivePacket:
        """Creates an IsAlivePacket based only on rsvd0 and rsvd1.
        
        Args:
            rsvd0 (uint32): Reserved field. For details see server
                documentation. The default is 0 (mostly used).
            rsvd1 (uint32): Reserved field. For details see server
                documentation. The default is 0 (mostly used).

        Returns:
            IsAlivePacket: Packet, that was created by using two uint32.

        Raises:
            struct.error: Either rsvd0 or rsvd1 is not uint32.
        """
        length = Header.totalSize + IsAlivePayload.totalSize
        header = Header(PacketType.ISALIVE, DeviceType.NONE, deviceId=0,
            length=length, connection=0)
        payload = IsAlivePayload(rsvd0, rsvd1)
        return IsAlivePacket(header, payload)