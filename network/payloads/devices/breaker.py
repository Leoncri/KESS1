from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.payloads.payload import Payload

class BreakerCommand(IntEnum):
    """Actions the breaker can execute
    
    Values:
        RESET: Reset the breaker
        GETDATA: Request the status of the breaker
        CLOSE: Close the breaker
        OPEN: Open the breaker

    TODO:
    - description of GETDATA correct?
    """
    RESET = int("0x0001", 16)
    GETDATA = int("0x0002", 16)
    CLOSE = int("0x0011", 16)
    OPEN = int("0x0012", 16)

class BreakerResult(IntEnum):
    """Available results of the actions of a breaker

    Values:
        SUCCESS: The requested action was successful.
        DATA: The requested action was successful and the respond contains
            the status information.
        FAILURE: The requested action wasn't successful.
        LOCKED: The requested action can't be executed. The breaker is
            executing another action. Resend the requested actions later.
        TIMEOUT: The requested actions can't be executed, since server couldn't
            reach the breaker.

    TODO:
    - description of DATA correct?
    """
    SUCCESS = int("0x0001", 16)
    DATA = int("0x0002", 16)
    FAILURE = int("0x0100", 16)
    LOCKED = int("0x0101", 16)
    TIMEOUT = int("0x0102", 16)

@dataclass
class BreakerStatusPayload(Payload):
    """Payload to describe the status of a breaker.
    
    Attributes:
        _typeFormatString (string): Format string of additional fields.
        fullTypeFormatString (string): Format string of all fields.
        size (int): Additional bytes required by added fields.
        totalSize (int): Number of bytes required in total by all fields.

    Fields:
        status (uint32): Status of the breaker
        voltageNode1 (float): Voltage at node 1 in V
        voltageNode2 (float): Voltage at node 2 in V
        current (float): Current in A
    """
    _typeFormatString = "Ifff"
    fullTypeFormatString = Payload.fullTypeFormatString + _typeFormatString
    _typeFormatString = Payload._byteOrder + _typeFormatString
    size = struct.calcsize(_typeFormatString)
    totalSize = struct.calcsize(fullTypeFormatString)

    status : int = field(default=0)
    voltageNode1 : float = field(default=0)
    voltageNode2 : float = field(default=0)
    current : float = field(default=0)

    def GetBytes(self) -> bytearray:
        """Gives the binary representation of the BreakerStatusPayload
        
        Returns:
            bytearray: Binary representation of the fields.
            
        Raises:
            struct.error: The type of at least one field doesn't match with
                _typeFormatString or the value exceeds the expected range.
        """
        breakerStatusBytes = struct.pack(BreakerStatusPayload._typeFormatString,
            self.status, self.voltageNode1, self.voltageNode2, self.current)
        return breakerStatusBytes

    def ParseBytes(breakerBytes: bytearray) -> tuple[int, float, float, float]:
        """Retrieves status, voltageNode1, voltageNode2, current from a
        bytearray.
        
        Args:
            breakerBytes (bytearray): Binary data of the fields. Only bytes
                from 0 to size (exclusive) are considered. Further bytes don't
                have an effect.
        
        Returns:
            A tuple representing (status, voltagenode1, voltageNode2, current)

        Raises:
            IndexError: Number of bytes in breakerBytes is insufficient for 
                creating BreakerStatusPayload.
        """
        if len(breakerBytes) < BreakerStatusPayload.size:
            raise IndexError("Error: Too few bytes for a BreakerStatusPayload.")
        breakerBytes = breakerBytes[:BreakerStatusPayload.size]
        return struct.unpack(BreakerStatusPayload._typeFormatString, breakerBytes)

    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes: bytearray) -> BreakerStatusPayload:
        """Creates a BreakerStatusPayload based on binary data.
        
        Args:
            payloadBytes (bytearray): Binary data the BreakerStatusPayload is
                retrieved from.
        
        Returns:
            BreakerStatusPayload: The retrieved payload.

        Raises:
            struct.error: At least one of the types doesn't match with those
                specified in the _typeFormatString or exceeds the range of the
                type.
            IndexError: The number of bytes supplied by payloadBytes is insufficient
                to create a BreakerStatusPayload.
        """
        (status, voltageNode1, voltageNode2, current)= cls.ParseBytes(payloadBytes)
        return BreakerStatusPayload(status, voltageNode1, voltageNode2,
            current)
