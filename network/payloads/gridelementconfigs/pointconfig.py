from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType

@dataclass
class PointConfig(GridElementConfig):
    """Represent a point
    
    In contrast to nodes, points contain spatial information (x and y).
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        nodeId (uint16): Id of the node, which the point represents
        rsvd (uint16): 
        posX (uint32): Horizontal position in the GUI (starts in upper left
            corner)
        posY (uint32): Vertical position in the GUI (start in upper left
            corner)

    TODO:
    - Add description for rsvd
    """
    _typeFormatString = "HHHH"
    fullTypeFormatString = (GridElementConfig.fullTypeFormatString +
        _typeFormatString)
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.POINT, init=False)
    
    nodeId : int = field(default=0)
    rsvd : int = field(default=0)
    posX: int = field(default=0)
    posY: int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the PointConfig.
        
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
        pointConfigBytes = struct.pack(PointConfig._typeFormatString,
            self.nodeId, self.rsvd, self.posX, self.posY)
        unpadded = gridElementConfigBytes + pointConfigBytes
        return self.FillUpGridElementConfig(unpadded)

    def ParseBytes(pointConfigBytes: bytearray) -> tuple[int, int, int, int]:
        """Retrieves the fields of a PointConfig from a bytearray.
        
        Args:

            pointConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (nodeId, rsvd, posX, posY)
            
        Raises:
            IndexError: Number of bytes in pointConfigBytes is insufficient for
                creating a PointConfig
        """
        if len(pointConfigBytes) < PointConfig.size:
            raise IndexError("Error: Too few bytes for a PointConfig")
        pointConfigBytes = pointConfigBytes[:PointConfig.size]
        pointConfigTuple = struct.unpack(PointConfig._typeFormatString,
            pointConfigBytes)
        return pointConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> PointConfig:
        """Creates a PointConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the PointConfig is retrieved
                from.
        
        Returns:
            PointConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a PointConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        pointConfigBytes = payloadBytes[GridElementConfig.size:]
        (_, id) = super().ParseBytes(gridElementConfigBytes)
        (nodeId, rsvd, posX, posY) = cls.ParseBytes(pointConfigBytes)
        return cls(id, nodeId, rsvd, posX, posY)
    
    @classmethod
    def GetPayloadFromConfig(cls, config : dict) -> PointConfig:
        # get data from config
        posX = config["positionX"]
        posY = config["positionY"]
        type = config["electricalType"]
        id = config["id"]
        nodeId = config["nodeId"]
        
        return cls(id=id, nodeId=nodeId, rsvd=0, posX=posX, posY=posY)