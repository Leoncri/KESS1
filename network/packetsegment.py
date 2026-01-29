from dataclasses import *

class PacketSegment:

    _byteOrder = "<"

    def __post_init__(self) -> None:
        """
        Validate the field's data by creating a byte represensation. 

        Errors:
            Raises struct.error, if the format string and the data don't
            matchup.
        """
        self.GetBytes()

    def ParseBytes(packetBytes: bytearray) -> None:
        pass

    def GetFullFormatString(self) -> str:
        """
        Returns the full format string including the symbol for the byte order
        and the format strings of the parents.

        Example:
            byteOrder = "<", parentFormat = "H", childFormat = "I"
            GetFullFormatString() will return "<HI"
        """
        return type(self).fullTypeFormatString

    def GetFormatString(self) -> str:
        """
        Returns only the format string for the additional types implemented by
        that class and the symbol for the byte order.

        Example:
            byteOrder = "<", parentFormat = "H", childFormat = "I"
            GetFormatString will() return "<HI"
        """
        return type(self)._typeFormatString

    def GetSize(self) -> int:
        """
        Number of bytes required for the additional fields implemented by
        that class. The field size of the parent class is not considered here.
        
        Example:
            parentFormat = "H", actualFormat = "I"
            GetSize() = 4
        """
        return type(self).size

    def GetTotalSize(self) -> int:
        """
        Number of bytes required for all fields implemented by that class
        and its parents.

        Example:
            parentFormat = "H", actualFormat = "I"
            GetTotalSize() = 6
        """
        return type(self).totalSize

    def GetBytes(self) -> bytearray:
        """
        Overriden by their inherited class. There, it converts the packet
        into a bytearray representation with respect to the _byteOrder and
        their types specified in _typeFormatString.

        Returns:
            A bytearray representing the object in ctype compatible form.
        """
        pass

    def UpdateSlicingIndices(oldStartIndex: int, oldEndIndex: int,
            length: int) -> tuple[int, int]:
        """
        Calculates the slice positions in a byte array.

        Args:
            oldStartIndex (int): Start position in the byte array (inclusive)
            oldEndIndex (int): End position in the byte array(exclusive)

        Returns:
            The tuple of the new positions represented as integers:
            (newStart, newEnd). newEnd is not included.
            
        """

        newStartIndex = oldEndIndex
        newEndIndex = newStartIndex + length

        return (newStartIndex, newEndIndex)