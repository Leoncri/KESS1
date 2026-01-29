from __future__ import annotations
from dataclasses import *
import struct

from .gridelementconfig import GridElementConfig
from .elementtype import ElementType

@dataclass
class NodeConfig(GridElementConfig):
    """Represents a node

    In contrast to points, nodes don't contain spatial information (x or y).

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        nodeType (uint16):
        rsvd (uint16):
    
    TODO:
    - What kind of value is stored in nodeType? Are new enums required?
    - Add description for nodeType and rsvd in documentation
    """
    _typeFormatString = "HH"
    fullTypeFormatString = GridElementConfig.fullTypeFormatString + _typeFormatString
    _typeFormatString = GridElementConfig._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    elementType : ElementType = field(default=ElementType.NODE, init=False)
    nodeType : int = field(default=0)
    rsvd : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the NodeConfig.
        
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
        nodeConfigBytes = struct.pack(NodeConfig._typeFormatString, self.nodeType, self.rsvd)
        
        unpadded = gridElementConfigBytes + nodeConfigBytes
        return self.FillUpGridElementConfig(unpadded)
    
    def ParseBytes(nodeConfigBytes: bytearray) -> tuple[int]:
        """Retrieves nodeType and rsvd from a bytearray.
        
        Args:
            nodeConfigBytes (bytearray): Binary data of the fields of this
                class. The fields of the parent class are not included.
                Only bytes from 0 to size (exlusive) are considered. Further
                bytes don't have an effect.
                
        Returns:
            A tuple representing (nodeType, rsvd)
            
        Raises:
            IndexError: Number of bytes in nodeConfigBytes is insufficient for
                creating NodeConfig
        """
        if len(nodeConfigBytes) < NodeConfig.size:
            raise IndexError("Error: Too few bytes for a NodeConfig")
        
        nodeConfigBytes = nodeConfigBytes[:NodeConfig.size]
        nodeConfigTuple = struct.unpack(NodeConfig._typeFormatString, nodeConfigBytes)
        
        return nodeConfigTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> NodeConfig:
        """Creates a NodeConfig based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the NodeConfig is retrieved
                from.
        
        Returns:
            NodeConfig: The retrieved payload
            
        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is
                insufficient to create a NodeConfig.
        """
        gridElementConfigBytes = payloadBytes[:GridElementConfig.size]
        nodeConfigBytes = payloadBytes[GridElementConfig.size:]
        (_, id) = super().ParseBytes(gridElementConfigBytes)
        (nodeType, rsvd) = cls.ParseBytes(nodeConfigBytes)
        return cls(nodeType=nodeType, id=id, rsvd=rsvd)