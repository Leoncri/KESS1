from dataclasses import *
import struct

from .payload import Payload

@dataclass
class CommandRespondPayload(Payload):
    # internal variables
    _typeFormatString = "II"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    result : int = field(default=0)
    commandId: int = field(default=0)
    
    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the CommandRespondPayload.
        
        Returns:
            bytearray: Binary representation of the fields.
            
        Raises:
            struct.error: The type of one of the fields doesn't match with
                _typeFormatString or the values are not within the expected
                range.
        """
        return struct.pack(CommandRespondPayload._typeFormatString, self.rsvd0, self.rsvd1)
    
    def ParseBytes(respondPayloadBytes: bytearray) -> tuple[int, int]:
        """Retrieves error and rsvd0 from binary data.
        
        Args:
            respondPayloadBytes (bytearray): Binary data of the fields. Only
                bytes from 0 to size (exclusive) are considered. Further
                bytes don't have an effect.
        
        Returns:
            A tuple representing (error, rsvd0)

        Raises:
            IndexError: Number of bytes in respondPayloadBytes is insufficient
                for creating an CommandRespondPayload.
        """
        if len(respondPayloadBytes) < CommandRespondPayload.totalSize:
            raise IndexError("Error: Too few bytes for an ErrorHeader.")
        
        respondPayloadTuple = struct.unpack(CommandRespondPayload._typeFormatString,
            respondPayloadBytes)
        return respondPayloadTuple

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray):
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
        return CommandRespondPayload(error, rsvd0)