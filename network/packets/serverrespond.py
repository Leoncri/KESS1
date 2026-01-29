from __future__ import annotations

from network.packets.packet import Packet
from network.headers.header import Header, DeviceType, PacketType

from network.headers.commandrespond import CommandRespondHeader

from network.payloads.serverrespond import ServerStatusPayload

class ServerStatusPacket(Packet):
    def __init__(self, header : CommandRespondHeader, payload : ServerStatusPayload):
        super().__init__(header, payload)