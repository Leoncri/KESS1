from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType
from auxillary.iphelper import *

@dataclass
class ConverterConfig(GridElementConfig):
    """Represents a converter
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields:
        point1Id (uint16): Id of point in left corner
        point2Id (uint16): Id of point in right corner
        config (uint16): 
        port (uint16): Port, which the converter uses to communicate with the
            server.
        ip (uint32): Ip address, which the converter uses to communicate with
            the server.
    
    TODO:
    - Add description to field config
    """
    _typeFormatString = "HHHHIHHHH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString +
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.CONVERTER, init=False)
        
    point1Id : int = field(default=0)
    point2Id : int = field(default=0)
    config : int = field(default=0)
    port : int = field(default=0)
    ip: string = field(default="")
    posX : int = field(default=0)
    posY : int = field(default=0)
    rotation : int = field(default=0)
    rsvd : int = field(default=0, init=False)
    name : string = field(default="")

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the ConverterConfig.
        
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
        converterConfigBytes = struct.pack(ConverterConfig._typeFormatString,
                self.point1Id, self.point2Id, self.config, self.port,
                ip, self.posX, self.posY, self.rotation, self.rsvd)
        
        if len(self.name) > 23:
            self.name = self.name[:23]
        byteName = bytearray(self.name.encode('utf-8'))
        
        unpadded = gridElementConfigBytes + converterConfigBytes + byteName
        return self.FillUpGridElementConfig(unpadded)

    def ParseBytes(converterConfigBytes: bytearray) -> tuple[int, int, int, int, int, int, int, int, int]:
        """Retrieves the fields from a bytearray.
        
        Args:
            converterConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (pointId1, pointId2, config, port, ip)
            
        Raises:
            IndexError: Number of bytes in converterConfigBytes is insufficient for
                creating ConverterConfig
        """
        if len(converterConfigBytes) < ConverterConfig.size:
            raise IndexError("Error: Too few bytes  for a ConverterConfig")
        
        converterConfigBytes = converterConfigBytes[:ConverterConfig.size]
        converterConfigTuple = struct.unpack(ConverterConfig._typeFormatString, converterConfigBytes)
        
        return converterConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> ConverterConfig:
        """Creates a ConverterConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the ConverterConfig is retrieved
                from.
        
        Returns:
            ConverterConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a ConverterConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        converterConfigBytes = payloadBytes[GridElementConfig.size:]
        converterName = converterConfigBytes[ConverterConfig.size:]
        
        print (converterName)
        name = converterName.decode('utf-8').rstrip('\x00')
        print (name)
        
        (_, id) = super().ParseBytes(gridElementConfigBytes)
        (point1Id, point2Id, config, port, ip, posX, posY, rotation, _) = cls.ParseBytes(converterConfigBytes)
        return cls(id, point1Id, point2Id, config, port, Int2IP(ip), posX, posY, rotation, name)
