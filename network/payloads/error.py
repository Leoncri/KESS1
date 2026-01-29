from __future__ import annotations
from dataclasses import *
import struct
from enum import IntEnum

from .payload import Payload

class ErrorType(IntEnum):
    """Named error types
    
    Values:
        UNSUPPORTED:

    TODO:
    - add proper description for ErrorType UNSUPPORTED
    - add proper description for rsvd0
    """
    UNSUPPORTED = int("0x01", 16)

@dataclass
class ErrorPayload(Payload):
    """Payload to give further details about the occured error.
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        error (uint32): Describes the kind of error, which occured.
            Accepts the in ErrorType specified ErrorTypes, their
            corresponding integers values or any other integer in the
            uint32 range (ensure the server supports that type of error).
        rsvd0 (uint32): Reserved space for further information. See
            server implementation for further details.
    """
    _typeFormatString = "II"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    error : int = field(default=ErrorType.UNSUPPORTED)
    rsvd0 : int = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the ErrorPayload.
        
        Returns:
            bytearray: Binary representation of the fields.
        
        Raises:
            struct.error: The type of one of the fields doesn't match with
                _typeFormatString or the values are not within the expected
                range.
        """
        return struct.pack(ErrorPayload._typeFormatString, self.error,
            self.rsvd0)
    
    def ParseBytes(errorPayloadBytes: bytearray) -> tuple[int, int]:
        """Retrieves error and rsvd0 from binary data.
        
        Args:
            errorPayloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
        
        Returns:
            A tuple representing (error, rsvd0)

        Raises:
            IndexError: Number of bytes in errorPayloadBytes is insufficient
                for creating an ErrorPayload.
        """
        if len(errorPayloadBytes) < ErrorPayload.totalSize:
            raise IndexError("Error: Too few bytes for an ErrorHeader.")
        
        errorPayloadTuple = struct.unpack(ErrorPayload._typeFormatString,
            errorPayloadBytes)
        return errorPayloadTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> ErrorPayload:
        """Creates an ErrorPayload based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
        
        Returns:
            ErrorPayload: The retrieved Payload.
            
        Raises:
            IndexError: Number of bytes in errorPayloadBytes is insufficient
                for creating an ErrorPayload.
        """
        (error, rsvd0) = cls.ParseBytes(payloadBytes)
        return ErrorPayload(error, rsvd0)