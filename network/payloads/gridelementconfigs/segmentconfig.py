from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType

@dataclass
class SegmentConfig(GridElementConfig):
    """Represents a segment (the connection line between to points).
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
    
    Fields:
        point1Id (uint16): Id of the first point
        point2Id (uint16): Id of the second point       
    """
    _typeFormatString = "HH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString +
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.SEGMENT, init=False)
    
    point1Id: int = field(default=0)
    point2Id: int = field(default=0)

    def GetBytes(self) ->bytearray:
        """Gives the binary representation of the SegmentConfig.
        
        The fields elementType and id are included.

        Returns:
            bytearray: Binary representation of the fields. The length is
            always _maxTotalSize (see GridElementConfig for details) and
            the difference is filled up with zero bytes.

        Raises:
            struct.error: The type of at least one field doesn't match with
                _typeFormatString or the value exceeds the expected range.
        """
        nodeConfigBytes = super().GetBytes()
        segmentConfigBytes = struct.pack(SegmentConfig._typeFormatString,
            self.point1Id, self.point2Id)
        unpadded = nodeConfigBytes + segmentConfigBytes
        return self.FillUpGridElementConfig(unpadded)

    def ParseBytes(segmentConfigBytes : bytearray) -> tuple[int, int]:
        """Retrieves the fields of a SegmentConfig from a bytearray.
        
        Args:

            segmentConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (point1Id, point2Id)
            
        Raises:
            IndexError: Number of bytes in pointConfigBytes is insufficient for
                creating a SegmentId
        """
        if len(segmentConfigBytes) < SegmentConfig.size:
            raise IndexError("Error: Too few bytes for a SegmentConfig")
        segmentConfigBytes = segmentConfigBytes[:SegmentConfig.size]
        segmentConfigTuple = struct.unpack(SegmentConfig._typeFormatString,
            segmentConfigBytes)
        return segmentConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> SegmentConfig:
        """Creates a SegmentConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the SegmentConfig is retrieved
                from.
        
        Returns:
            SegmentConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a SegmentConfig.
        """
        nodeConfigBytes = payloadBytes[:GridElementConfig.size]
        segmentConfigBytes = payloadBytes[GridElementConfig.size:]
        (_, id) = super().ParseBytes(nodeConfigBytes)
        (point1Id, point2Id) = cls.ParseBytes(segmentConfigBytes)
        return cls(id, point1Id, point2Id)
    
    @classmethod
    def GetPayloadFromConfig(cls, config : dict) -> SegmentConfig:
        # get data from segment
        point1Id = config["point1Id"]
        point2Id = config["point2Id"]
        
        return cls(id=0, point1Id=point1Id, point2Id=point2Id)