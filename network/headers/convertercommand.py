from __future__ import annotations
from dataclasses import *
from enum import IntEnum
import struct

from network.packetsegment import PacketSegment
from network.headers.header import DeviceType
from network.headers.command import CommandHeader

class ConverterConfigValues(IntEnum):
    # config for converter creation
    CONFIG_USE_ADS  = int("0x1", 16)

class ConverterStatus(IntEnum):
    # staus bits
    STATUS_OK       = int("0x1", 16)
    STATUS_WARNING  = int("0x2", 16)
    STATUS_ERROR    = int("0x4", 16)
    STATUS_MISSING_LIGHTLOOP    = int("0x8", 16)

class ConverterStatusNames:
    names = [
        "OK\n",
        "Warning\n",
        "Error\n",
        "Missing Lightloop\n"
    ]

class ConverterWarnings(IntEnum):
    # warning bits
    WARNING_TEMP    = int("0x1", 16)

class ConverterErrors(IntEnum):
    # error bits
    ERROR_TEMP          = int("0x01", 16)
    ERROR_OVERVOLTAGE_1 = int("0x02", 16)
    ERROR_OVERVOLTAGE_2 = int("0x04", 16)
    ERROR_OVERCURRENT_1 = int("0x08", 16)
    ERROR_OVERCURRENT_2 = int("0x10", 16)

class ConverterModes(IntEnum):
    # all modes
    MODE_OFF                = 1
    MODE_IDLE               = 2
    MODE_VOLTAGE_CONTROL_1  = 3
    MODE_VOLTAGE_CONTROL_2  = 4
    MODE_DROOP_CONTROL_1    = 5
    MODE_DROOP_CONTROL_2    = 6
    MODE_POWER_CONTROL      = 7
    MODE_PRECHARGE_1        = 8
    MODE_PRECHARGE_2        = 9
    MODE_DISCHARGE_1        = 10
    MODE_DISCHARGE_2        = 11
    MODE_RESET              = 255

class ConverterModeNames:
    names = [
        "Not valid",
        "Off",
        "Idle",
        "Voltage control side 1",
        "Voltage control side 2",
        "Droop control side 1",
        "Droop control side 2",
        "Power control",
        "Precharge side 1",
        "Precharge side 2",
        "Discharge side 1",
        "Discharge side 2"]

class ConverterAvailableModes(IntEnum):
    # available modes
    MODE_AV_VOLTAGE_CONTROL_1   = int("0x004", 16)
    MODE_AV_VOLTAGE_CONTROL_2   = int("0x008", 16)
    MODE_AV_DROOP_CONTROL_1     = int("0x010", 16)
    MODE_AV_DROOP_CONTROL_2     = int("0x020", 16)
    MODE_AV_POWER_CONTROL       = int("0x040", 16)
    MODE_AV_PRECHARGE_1         = int("0x080", 16)
    MODE_AV_PRECHARGE_2         = int("0x100", 16)
    MODE_AV_DISCHARGE_1         = int("0x200", 16)
    MODE_AV_DISCHARGE_2         = int("0x400", 16)

class ConverterCommand(IntEnum):
    SET_MODE            = int("0x0100", 16)
    UPDATE_DATA         = int("0x0200", 16)
    PERIODIC_DATA       = int("0x0300", 16)
    
    PERIODIC_DATA_ON    = int("0x0001", 16)
    PERIODIC_DATA_OFF   = int("0x0002", 16)

@dataclass
class ConverterCommandSetModeHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.CONVERTER, init=False)
    command : int = field(default=0)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(headerBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(headerBytes)

@dataclass
class ConverterCommandUpdateDataHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.CONVERTER, init=False)
    command : int = field(default=0)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(headerBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(headerBytes)

@dataclass
class ConverterCommandPeriodicDataOnHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.CONVERTER, init=False)
    command : int = field(default=ConverterCommand.PERIODIC_DATA | ConverterCommand.PERIODIC_DATA_ON)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(headerBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(headerBytes)

@dataclass
class ConverterCommandPeriodicDataOffHeader(CommandHeader):
    deviceType : DeviceType = field(default=DeviceType.CONVERTER, init=False)
    command : int = field(default=ConverterCommand.PERIODIC_DATA | ConverterCommand.PERIODIC_DATA_OFF)
    
    def GetBytes(self):
        # return the header bytes
        return super().GetBytes()
    
    def ParseBytes(headerBytes : bytearray):
        # returns the data inside the command header
        return super().ParseBytes(headerBytes)