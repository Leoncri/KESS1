from __future__ import annotations

from network.headers.header import PacketType, DeviceType
from network.headers.headerparser import HeaderParser
from network.headers.gridcommand import GridCommand
from network.headers.gridrespond import *
from network.headers.serverrespond import *

from network.packets.packet import Packet
from network.packets.gridconfig import GridConfigPacket
from network.packets.isalive import IsAlivePacket
from network.packets.error import ErrorPacket
from network.packets.genericrespond import GenericRespondPacket
from network.packets.gridconfigrespond import GridConfigSizeRespondPacket
from network.packets.gridconfigrespond import GridGetConfigRespondPacket
from network.packets.serverrespond import ServerStatusPacket
from network.packets.fenswitchgearrespond import *
from network.packets.converterrespond import *
from network.packets.scibreakbreakerrespond import *

from network.payloads.isalive import IsAlivePayload
from network.payloads.error import ErrorPayload
from network.payloads.devices.breaker import BreakerStatusPayload
from network.payloads.gridelementconfigs.gridelementconfigparser import GridElementConfigParser
from network.payloads.gridrespond import GridGetLengthRespondPayload
from network.payloads.gridrespond import GridGetConfigRespondPayload
from network.payloads.serverrespond import ServerStatusPayload
from network.payloads.fenswitchgearrespond import *
from network.payloads.converterrespond import *
from network.payloads.scibreakbreakerrespond import *

class PacketParser:
    """Collection of methods to retrieve an entire packet from binary data.
    
    Typical usage:

    parsedPacket = PacketParser.GetPacketFromBytes(packetBytes)

    TODO:
    - implement device data packet
    """

    @staticmethod
    def GetPacketFromBytes(packetBytes: bytearray) -> Packet:
        (header, lastRead) = HeaderParser.GetHeaderFromBytes(packetBytes)
        """Retrieves a packet from binary data.
        
        Args:
            packetBytes (bytearray): Entire binary data representing a single
                packet.
        
        Returns:
            A Packet (or a derived class) based on the binary data.
        
        Raises:
            IndexError: The number of bytes is insufficient for the anticipated
                packet.
        """
        payloadBytes = packetBytes[lastRead:]
        
        if header.packetType == PacketType.ISALIVE:
            payload = IsAlivePayload.GetPayloadFromBytes(payloadBytes)
            return IsAlivePacket(header, payload)
        
        elif header.packetType == PacketType.ERROR:
            payload = ErrorPayload.GetPayloadFromBytes(payloadBytes)
            return ErrorPacket(header, payload)
        
        elif header.packetType == PacketType.DEVICEDATA:
            # this returns packets containing live data from devices
            if header.deviceType == DeviceType.FENSWITCHGEAR:
                # create a new payload for the FEN switchgear device data
                payload = FENSwitchgearLiveDataPayload.GetPayloadFromBytes(payloadBytes)
                return FENSwitchgearLiveDataPacket(header, payload)
            
            elif header.deviceType == DeviceType.CONVERTER:
                # create a new payload for the converter device data
                payload = ConverterLiveDataPayload.GetPayloadFromBytes(payloadBytes)
                return ConverterLiveDataPacket(header, payload)
            
            elif header.deviceType == DeviceType.SCIBREAKBREAKER:
                # create a new payload for the SciBreak breaker device data
                payload = SciBreakBreakerLiveDataPayload.GetPayloadFromBytes(payloadBytes)
                return SciBreakBreakerLiveDataPacket(header, payload)
            
            print ("Unknown live data packet type")
            
            return None
        
        elif header.packetType == PacketType.RESPOND:
            # grid gets either a pure respond packet OR a GET_CONFIG_DATA
            if header.deviceType == DeviceType.GRID:
                if header.result == GridRespond.GET_CONFIG_DATA:
                    # create a grid data respond packet
                    payload = GridGetConfigRespondPayload.GetPayloadFromBytes(payloadBytes, header.numberGridElements)
                    return GridGetConfigRespondPacket(header, payload)
                elif header.result == GridRespond.GET_CONFIG_LENGTH:
                    # create a grid config length respond packet
                    payload = GridGetLengthRespondPayload.GetPayloadFromBytes(payloadBytes)
                    return GridConfigSizeRespondPacket(header, payload)
                else:
                    # create a generic respond packet
                    return GenericRespondPacket(header)
            # server get either a pure respond packet OR a STATUS_DATA
            elif header.deviceType == DeviceType.SERVER:
                if header.result == ServerRespond.STATUS_DATA:
                    # create a server status data packet
                    payload = ServerStatusPayload.GetPayloadFromBytes(payloadBytes)
                    return ServerStatusPacket(header, payload)
                else:
                    # create a generic repond packet
                    return GenericRespondPacket(header)
            
            elif header.deviceType == DeviceType.FENSWITCHGEAR:
                return GenericRespondPacket(header)
            
            elif header.deviceType == DeviceType.CONVERTER:
                return GenericRespondPacket(header)
            
            elif header.deviceType == DeviceType.SCIBREAKBREAKER:
                return GenericRespondPacket(header)