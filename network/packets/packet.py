from __future__ import annotations
from math import ceil

from network.payloads import *
from network.headers import *

class Packet:
    """Base class for all Packets.

    Attributes:
        maxPacketSize (int): Number of bytes a single packet (including header)
            can have
    
    Fields:
        
        header (Header): Contains structural information about the packet
            (e.g. packetType, deviceType, deviceId, ...). The explicit
            structure of the header depends on the used class (from Header
            derived classes are possible).
        payload (Payload): Contains the actual information. 
    """
    maxSizePacket = 1024
    def __init__(self, header: Header = None,
        payload : Payload = None) -> Packet:
        """Creates a Packet based on an existing header and and existing
        payload.

        Args:
            header (Header): Header (not derived class) is used to provide
                structural information (e.g. packetType, deviceType,
                deviceId, ...)
            payload (Payload): Contains the actual information.
        
        Return:
            Packet: Packet based on an existing header and an existing
                payload.
        """
        self.header = header
        self.payload = payload

    @staticmethod
    def AddPadding(unpaddedBinaryPacket : bytearray) -> bytearray:
        """Zero bytes are added at the end to ensure a packet length of n * 16

        Checks, if adding zero bytes is neccessary.
        
        Args:
            unpaddedBinaryPacket (bytearray): The packet in binary form, which
                may require padding.
            
        Returns:
            The binary representation of a packet, which has a length of
            multiples of 16.
        """
        nextMultiple = ceil(len(unpaddedBinaryPacket) / 16) * 16
        numberZeros = nextMultiple - len(unpaddedBinaryPacket)
        if numberZeros > 0:
            zeroPadding = bytearray(numberZeros)
            return unpaddedBinaryPacket + zeroPadding
        return unpaddedBinaryPacket

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the entire packet.

        All packets have a length of multiples of 16. If required, the end
        will be filled up with zero bytes. If the payload of the packet is
        None (e.g. sending a RespondHeader), only the binary representation
        of the header is returned.
        
        Return:
            bytearray: Binary representation of header and payload (in
                that order).
        """
        unpadded = self.header.GetBytes()
        if payload != None:
            unpadded += self.payload.GetBytes()
        padded = Packet.AddPadding(unpadded)
        return padded     

    def __eq__(self, packet: Packet) -> bool:
        """Checks itself with another packet on equality.
        
        Args:
            packet (Packet): Other packet, this packet shall be compared
            to.

        Return:
            bool: True, if self and packet are equal, false otherwise.
        """
        return (self.header == packet.header and
            self.payload == packet.payload)

    def __ne__(self, packet: Packet) -> bool:
        """Checks itself with another packet on inequality.
        
        Args:
            packet (Packet): Other packet, this packet shall be compared
            to.

        Return:
            bool: True, if self and packet are unequal, false otherwise.
        """
        return (self.header != packet.header and
            self.payload != packet.payload)

    def __repr__(self) -> str:
        """Returns a string representation of the packet in the following form:
        Packet(<Header>, <Payload>)."""
        headerRepr = self.header.__repr__()
        payloadRepr = self.payload.__repr__()
        repr = f"Packet({headerRepr}, {payloadRepr})"
        return  repr
