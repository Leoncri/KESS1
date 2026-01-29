from dataclasses import *
import struct

from .payload import Payload

@dataclass
class ServerStatusPayload(Payload):
    # internal variables
    _typeFormatString = "HHHHHHI"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    usedConnections : int = field(default=0)
    status : int = field(default=0)
    serverLoad : int = field(default=0)     # in 0.01% -> 10.000 = 100%
    connectedDevices : int = field(default=0)
    fileVersion : int = field(default=0)
    rsvd1 : int = field(default=0, init=False)
    rsvd2 : int = field(default=0, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the packed bytes
        return struct.pack(ServerStatusPayload._typeFormatString, self.usedConnections,
                            self.status, self.serverLoad, self.connectedDevices, self.fileVersion, self.rsvd1, self.rsvd2)
    
    def ParseBytes(statusPayloadBytes : bytearray) -> tuple[int, int, int, int, int]:
        # returns the data inside the payload
        if len(statusPayloadBytes) != ServerStatusPayload.totalSize:
            raise IndexError("Error: Too few bytes for a ServerStatusPayload.")
        
        connections, status, load, devices, version, _, __ = struct.unpack(ServerStatusPayload._typeFormatString, statusPayloadBytes)
        
        return (connections, status, load, devices, version)
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray):
        # get data from bytes
        connections, status, load, devices, version = cls.ParseBytes(payloadBytes)
        
        return ServerStatusPayload(usedConnections=connections, status=status, serverLoad=load, connectedDevices=devices, fileVersion=version)