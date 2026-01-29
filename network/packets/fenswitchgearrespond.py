from __future__ import annotations
import random

from network.headers.devicedata import DeviceDataHeader

from network.packets.packet import Packet

class FENSwitchgearLiveDataPacket(Packet):
    def __init__(self, header : DeviceDataHeader, payload : FENSwitchgearLiveDataPayload):
        super().__init__(header, payload)
    