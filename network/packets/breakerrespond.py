from __future__ import annotations
import random

from network.headers.devicedata import DeviceDataHeader

from network.packets.packet import Packet

class SciBreakBreakerLiveDataPacket(Packet):
    def __init__(self, header : DeviceDataHeader, payload : SciBreakBreakerLiveDataPayload):
        super().__init__(header, payload)