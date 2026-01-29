from __future__ import annotations
import random

from network.headers.devicedata import DeviceDataHeader

from network.packets.packet import Packet

class ConverterLiveDataPacket(Packet):
    def __init__(self, header : DeviceDataHeader, payload : ConverterLiveDataPayload):
        super().__init__(header, payload)