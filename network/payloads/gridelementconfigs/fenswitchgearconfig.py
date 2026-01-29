from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType
from auxillary.iphelper import *

@dataclass
class FENSwitchgearConfig(GridElementConfig):
    """Represents an FENSwitchgearConfig
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields:
        point1Id (uint16): Id of point in upper left corner
        point2Id (uint16): Id of point in bottom left corner
        point3Id (uint16): Id of point in upper right corner
        point4Id (uint16): Id of point in bottom right corner
        ip (uint32): Local ip address of FENSwitchgear
    """
    _typeFormatString = "HHHHHHIHHHH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString + 
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.FENSWITCHGEAR, init=False)

    point1Id: int = field(default=0)
    point2Id: int = field(default=0)
    point3Id: int = field(default=0)
    point4Id: int = field(default=0)
    port    : int = field(default=0)
    config  : int = field(default=0)
    ip      : string = field(default="")
    posX    : int = field(default=0)
    posY    : int = field(default=0)
    rotation: int = field(default=0)
    rsvd    : int = field(default=0)
    name    : string = field(default = "")

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the FENSwitchgearConfig.
        
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
        FENSwitchgearConfigBytes = struct.pack(
            FENSwitchgearConfig._typeFormatString, self.point1Id,
            self.point2Id, self.point3Id, self.point4Id, self.port, self.config, ip,
            self.posX, self.posY, self.rotation, self.rsvd)
        
        if len(self.name) > 19:
            self.name = self.name[:19]
        byteName = bytearray(self.name.encode('utf-8'))
        
        unpadded = gridElementConfigBytes + FENSwitchgearConfigBytes + byteName
        return self.FillUpGridElementConfig(unpadded)

    def ParseBytes(FENSwitchgearConfigBytes : bytearray) -> (
        tuple[int, int, int, int, int, int, int, int, int, int, int]):
        """Retrieves the fields from a bytearray.
        
        Args:
            FENSwitchgearConfigBytes (bytearray): Binary data of the fields of
                this class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (point1Id, point2Id, point3Id, point4Id, ip)
            
        Raises:
            IndexError: Number of bytes in FENSwitchgearConfigBytes is insufficient
                for creating FENSwitchgearConfig
        """
        if len(FENSwitchgearConfigBytes) < FENSwitchgearConfig.size:
            raise IndexError("Error: Too few bytes for a FENSwitchgearConfig")
        FENSwitchgearConfigBytes = FENSwitchgearConfigBytes[:FENSwitchgearConfig.size]
        
        FENSwitchgearConfigTuple = struct.unpack(FENSwitchgearConfig._typeFormatString, FENSwitchgearConfigBytes)
        
        return FENSwitchgearConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls,
        payloadBytes: bytearray) -> FENSwitchgearConfig:
        """Creates an FENSwitchgear based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the FENSwitchgearConfig
            is retrieved from.
        
        Returns:
            FENSwitchgearConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a FENSwitchgearConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        FENSwitchgearConfigBytes = payloadBytes[GridElementConfig.size:]
        FENSwitchgearName = FENSwitchgearConfigBytes[FENSwitchgearConfig.size:]
        
        print (FENSwitchgearName)
        name = FENSwitchgearName.decode('utf-8').rstrip('\x00')
        print (name)

        (_, id) = super().ParseBytes(gridElementConfigBytes)
        (point1Id, point2Id, point3Id, point4Id, port, config, ip, posX, posY, rotation, rsvd) = (
            cls.ParseBytes(FENSwitchgearConfigBytes))
        return cls(id, point1Id, point2Id, point3Id,
            point4Id, port, config, Int2IP(ip), posX, posY, rotation, rsvd, name)