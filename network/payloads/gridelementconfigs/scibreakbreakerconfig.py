from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType
from auxillary.iphelper import *

@dataclass
class SciBreakBreakerConfig(GridElementConfig):
    """Represents a breaker
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields:
        point1Id (uint16): Id of point in left corner
        point2Id (uint16): Id of point in right corner
        port (uint16): Port, which the breaker uses to communicate with
            the server.
        config (uint16):
        ip (uint32): Ip address, which the breaker uses to communicate with
            the server.
    TODO:
    - Add description of field config
    """
    _typeFormatString = "HHHHIHHHH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString + 
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.SCIBREAKBREAKER, init=False)

    point1Id: int = field(default=0)
    point2Id: int = field(default=0)
    config : int = field(default=0)
    port: int = field(default=0)
    ip: string = field(default="")
    posX : int = field(default=0)
    posY : int = field(default=0)
    rotation : int = field(default=0)
    rsvd : int = field(default=0)
    name : string = field(default="")

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the SciBreakBreakerConfig.
        
        The fields elementType and id are included.

        Returns:
            bytearray: Binary representation of the fields. The length is
            always _maxTotalSize (see GridElementConfig for details) and
            the difference is filled up with zero bytes.

        Raises:
            struct.error: The type of at least one field doesn't match with
                _typeFormatString or the value exceeds the expected range.
        """
        gridElementConfigBytes = super().GetBytes()
        ip = IP2Int(self.ip)
        breakerConfigBytes = struct.pack(SciBreakBreakerConfig._typeFormatString, 
            self.point1Id, self.point2Id, self.config, self.port, ip,
            self.posX, self.posY, self.rotation, self.rsvd)
        
        if len(self.name) > 23:
            self.name = self.name[:23]
        byteName = bytearray(self.name.encode('utf-8'))
        
        unpadded = gridElementConfigBytes + breakerConfigBytes + byteName
        return self.FillUpGridElementConfig(unpadded)

    def ParseBytes(breakerConfigBytes: bytearray) -> tuple[int, int, int, int, int, int, int, int, int]:
        """Retrieves the fields from a bytearray.
        
        Args:
            breakerConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (pointId1, pointId2, port, config, ip)
            
        Raises:
            IndexError: Number of bytes in breakerConfigBytes is insufficient for
                creating BreakerConfigBytes
        """
        if len(breakerConfigBytes) < SciBreakBreakerConfig.size:
            raise IndexError("Error: Too few bytes for a SciBreakBreakerConfig")
        breakerConfigBytes = breakerConfigBytes[:SciBreakBreakerConfig.size]
        breakerConfigTuple = struct.unpack(SciBreakBreakerConfig._typeFormatString,
            breakerConfigBytes)
        return breakerConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> SciBreakBreakerConfig:
        """Creates a SciBreakBreakerConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the SciBreakBreakerConfig is retrieved
                from.
        
        Returns:
            SciBreakBreakerConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a SciBreakBreakerConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        breakerConfigBytes = payloadBytes[GridElementConfig.size:]
        breakerName = payloadBytes[SciBreakBreakerConfig.size:]
        
        name = breakerName.decode('utf-8').rstrip('\x00')
        
        (_, id)  = super().ParseBytes(gridElementConfigBytes)
        (point1Id, point2Id, config, port, ip, posX, posY, rotation, rsvd) = cls.ParseBytes(
            breakerConfigBytes)
        
        return cls(id, point1Id, point2Id, config, port, Int2IP(ip), posX, posY, rotation, rsvd, name)