from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.command import CommandHeader

class ServerCommand(IntEnum):
    # some values for server commands
    START_GRID = int("0x0001", 16)
    STOP_GRID = int("0x0002", 16)

@dataclass
class ServerCommandStartGridHeader(CommandHeader):
    # header for starting the grid
    deviceType : int = field(default=DeviceType.SERVER, init=False)
    command : int = field(default=ServerCommand.START_GRID, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for starting the grid
        return super().GetBytes()
    
    def ParseBytes(serverHeaderBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(serverHeaderBytes)

@dataclass
class ServerCommandStopGridHeader(CommandHeader):
    # header for stopping the grid
    deviceType : int = field(default=DeviceType.SERVER, init=False)
    command : int = field(default=ServerCommand.STOP_GRID, init=False)
    
    def GetBytes(self) -> bytearray:
        # returns the bytearray for starting the grid
        return super().GetBytes()
    
    def ParseBytes(serverHeaderBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(serverHeaderBytes)