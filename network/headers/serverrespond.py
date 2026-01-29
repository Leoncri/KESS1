from enum import IntEnum

class ServerRespond(IntEnum):
    _fault = int("0x0100", 16)

    SUCCESS = int("0x0001", 16)
    STATUS_DATA = int("0x0010", 16)
    
    UNKNOWN_COMMAND = int("0x0001", 16) | _fault