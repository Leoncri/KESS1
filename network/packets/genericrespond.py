from network.packets.packet import Packet
from network.headers.header import Header, PacketType, DeviceType

from network.payloads.commandrespond import CommandRespondPayload

class GenericRespondPacket(Packet):
    def __init__(self, header : Header) -> None:
        super().__init__(header, None)