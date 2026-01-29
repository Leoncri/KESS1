# Return type hint of a method can be the type of the enclosing class
from __future__ import annotations
from dataclasses import *
import struct

from network.payloads.payload import Payload
from .elementtype import ElementType

@dataclass
class GridElementConfig(Payload):
    """Base class NodeConfig, PointConfig, ... are derived from.

    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.
        _maxTotalSize (int): The maximum number of bytes, any GridElementConfig
            requires. If fields of derived classes are adjusted or extended,
            please check, if this value must be changed too.

    Fields (added):
        elementType (uint16): Type of grid element. The default value is NODE.
        id (uint16): Id of the grid element. The default value is 0
    """

    _typeFormatString = "HH"
    fullTypeFormatString = (Payload.fullTypeFormatString + _typeFormatString)
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)
    maxTotalSize = 48

    elementType : ElementType = field(default=ElementType.NODE)
    id : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the byte representation for GridElementConfig.
        
        Returns:
        
            A tuple representing (elementType, id)
        
        Raises:
            struct.error: The type of one of the fields doesn't match with
                _TypeFormatString or the values are not within the expected
                range.
        """
        gridElementConfigBytes = struct.pack(
            GridElementConfig._typeFormatString,
            self.elementType, self.id)
        return gridElementConfigBytes

    def ParseBytes(gridElementConfigBytes : bytearray) -> tuple[ElementType]:
        """Retrieves the fields from a bytearray.

        Args:
            gridElementConfigBytes (bytearray): Binary data of the fields. Only the bytes
                from 0 to size (exclusive) are considered. Further bytes don't
                have an effect.
        
        Returns:
            A tuple representing (elementType, id)

        Raises:
            IndexError: Number of bytes in gridElementConfigBytes is
                insufficient for creating GridElementConfig.
        """
        if len(gridElementConfigBytes) < GridElementConfig.size:
            raise IndexError("Error: Too few bytes for a GridElementConfig")
        gridElementConfigBytes = (
            gridElementConfigBytes[:GridElementConfig.size])
        return struct.unpack(GridElementConfig._typeFormatString,
            gridElementConfigBytes)

    def FillUpGridElementConfig(self, gridElementConfigBytes : bytearray) -> bytearray:
        """Appends zero bytes to gridElementConfigBytes to always ensure
        a length of _maxTotalSize.
        
        Args:
            gridElementConfigBytes (bytearray): Binary data of a GridElementConfig
        
        Returns:
            A bytearray representation of the GridElementConfig with a
            guaranteed length of _maxTotalSize. The difference between
            totalSize and _maxTotalSize is filled with zero bytes.
        
        Raises:
            IndexError: gridElementBytes has more bytes than what is specified
                in GridElementConfig.maxTotalSize.
        """
        maxLength = GridElementConfig.maxTotalSize
        if len(gridElementConfigBytes) > maxLength:
            raise IndexError(f"Error: GridElementConfig is larger than {maxLength}")
        numberZerosRequired = (
            maxLength - len(gridElementConfigBytes))
        if numberZerosRequired > 0:
            padding = bytearray(numberZerosRequired)
            return gridElementConfigBytes + padding
        return gridElementConfigBytes