from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType

@dataclass
class SourceConfig(GridElementConfig):
    """
    This class represents a source inside the grid editor
    """
    
    _typeFormatString = "HHHH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString +
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.SOURCE, init=False)
    
    pointId : int = field(default=0)
    posX: int = field(default=0)
    posY: int = field(default=0)
    rotation : int = field(default=0)
    name : string = field(default="")
    
    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the SourceConfig.
        
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
        sourceConfigBytes = struct.pack(SourceConfig._typeFormatString,
            self.pointId, self.posX, self.posY, self.rotation)
        
        if len(self.name) > 36:
            self.name = self.name[:36]
        byteName = bytearray(self.name.encode('utf-8'))
        
        unpadded = gridElementConfigBytes + sourceConfigBytes + byteName
        return self.FillUpGridElementConfig(unpadded)
    
    def ParseBytes(sourceConfigBytes: bytearray) -> tuple[int, int, int, int]:
        """Retrieves the fields from a bytearray.
        
        Args:
            sourceConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (pointId, posX, posY, rotation)
            
        Raises:
            IndexError: Number of bytes in converterConfigBytes is insufficient for
                creating ConverterConfig
        """
        if len(sourceConfigBytes) < SourceConfig.size:
            raise IndexError("Error: Too few bytes for a SourceConfig")
        
        sourceConfigBytes = sourceConfigBytes[:SourceConfig.size]
        sourceConfigTuple = struct.unpack(SourceConfig._typeFormatString, sourceConfigBytes)
        
        return sourceConfigTuple
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> SourceConfig:
        """Creates a SourceConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the SourceConfig is retrieved
                from.
        
        Returns:
            SourceConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a ConverterConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        sourceConfigBytes = payloadBytes[GridElementConfig.size:]
        sourceName = converterConfigBytes[ConverterConfig.size:]
        
        #print (sourceName)
        name = sourceName.decode('utf-8').rstrip('\x00')
        #print (name)
        
        (_, id) = super().ParseBytes(gridElementConfigBytes)
        (pointId, posX, posY, rotation) = cls.ParseBytes(sourceConfigBytes)
        return cls(id, pointId, posX, posY, rotation, name)