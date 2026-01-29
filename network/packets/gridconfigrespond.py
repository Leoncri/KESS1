from __future__ import annotations

from network.packets.packet import Packet
from network.headers.header import Header, DeviceType, PacketType

from network.payloads.gridrespond import GridGetLengthRespondPayload

from network.headers.gridcommand import GridCommandLoadFileHeader

from network.payloads.gridelementconfigs import *

class GridConfigSizeRespondPacket(Packet):
    def __init__(self, header : Header, payload : GridGetLengthRespondPayload) -> None:
        super().__init__(header, payload)

class GridGetConfigRespondPacket(Packet):
    def __init__(self, header : GridCommandLoadFileHeader, payload : list[GridElementConfig]) -> GridGetConfigRespondPacket:
        super().__init__(header, payload)