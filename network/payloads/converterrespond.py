from __future__ import annotations
from dataclasses import *
import struct
from enum import IntEnum
from network.packetsegment import *

from .payload import Payload

from network.payloads.converterdata.statusdata import *
from network.payloads.converterdata.staticdata import *
from network.payloads.converterdata.voltagemeasurement import *
from network.payloads.converterdata.currentmeasurement import *
from network.payloads.converterdata.voltagecontrol import *
from network.payloads.converterdata.droopcontrol import *
from network.payloads.converterdata.powercontrol import *
from network.payloads.converterdata.precharge import *

class ConverterStatusBits(IntEnum):
    # bits defining the status of one converter
    ONLINE = int("0x01", 16)

class ConverterWarnings(IntEnum):
    #  defines for converter warnings
    WARNING_OVERTEMP    = int("0x1", 16)

class ConverterWarningMessages:
    Messages = [
        "Overtemperature\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n"]

class ConverterErrors(IntEnum):
    ERROR_OVERTEMP      = int("0x1", 16)
    ERROR_OVERVOLTAGE_1 = int("0x10", 16)
    ERROR_OVERVOLTAGE_2 = int("0x20", 16)
    ERROR_OVERCURRENT_1 = int("0x40", 16)
    ERROR_OVERCURRENT_2 = int("0x80", 16)

class ConverterErrorMessages:
    Messages = [
        "Overtemperature\n",
        "Missing Lightloop\n",
        "Doors Open\n",
        "EM OFF Pressed\n",
        "Overvoltage at side 1\n",
        "Overvoltage at side 2\n",
        "Overcurrent at side 1\n",
        "Overcurrent at side 2\n",
        "Overvoltage Midpoint at side 1\n",
        "Overvoltage Midpoint at side 2\n",
        "Error External Controller\n",
        "Error Internal\n",
        "Unused\n",
        "Unused\n",
        "Unused\n",
        "Unused\n"]

class ConverterLiveData(IntEnum):
    LIVE_DATA_LENGTH = 112

@dataclass
class ConverterLiveDataPayload(Payload):
    _typeFormatString = PacketSegment._byteOrder + "I"
    
    status              : int = field(default=0)
    rsvd                : int = field(default=0, init=False)
    statusDataSet       : ConverterStatusData = field(default=None)
    staticDataSet       : ConverterStaticData = field(default=None)
    voltageMeasurement  : ConverterVoltageData = field(default=None)
    currentMeasurement  : ConverterCurrentData = field(default=None)
    voltageControl1Data : ConverterVoltageControlData = field(default=None)
    voltageControl2Data : ConverterVoltageControlData = field(default=None)
    droopControl1Data   : ConverterDroopControlData = field(default=None)
    droopControl2Data   : ConverterDroopControlData = field(default=None)
    powerControlData    : ConverterPowerControlData = field(default=None)
    precharge1Data      : ConverterPrechargeData = field(default=None)
    precharge2Data      : ConverterPrechargeData = field(default=None)
    
    def ParseBytes(payloadBytes : bytearray):
        # check length
        print (len(payloadBytes))
        if len(payloadBytes) != ConverterLiveData.LIVE_DATA_LENGTH:
            raise IndexError("Error: Too few bytes for converter live data.")
        
        statusBits, = struct.unpack(ConverterLiveDataPayload._typeFormatString, payloadBytes[0:4])
        print (statusBits)
        
        converterStructure = payloadBytes[8:]
        
        # process the bytes
        statusData = ConverterStatusData.GetDataFromBytes(converterStructure[0:8])
        staticData = ConverterStaticData.GetDataFromBytes(converterStructure[8:16])
        voltageData = ConverterVoltageData.GetDataFromBytes(converterStructure[16:24])
        currentData = ConverterCurrentData.GetDataFromBytes(converterStructure[24:32])
        vControl1Data = ConverterVoltageControlData.GetDataFromBytes(converterStructure[48:56])
        vControl2Data = ConverterVoltageControlData.GetDataFromBytes(converterStructure[56:64])
        dControl1Data = ConverterDroopControlData.GetDataFromBytes(converterStructure[64:72])
        dControl2Data = ConverterDroopControlData.GetDataFromBytes(converterStructure[72:80])
        pControlData = ConverterPowerControlData.GetDataFromBytes(converterStructure[80:88])
        precharge1Data = ConverterPrechargeData.GetDataFromBytes(converterStructure[88:96])
        precharge2Data = ConverterPrechargeData.GetDataFromBytes(converterStructure[96:104])
        
        return (statusBits, statusData, staticData, voltageData, currentData, vControl1Data, vControl2Data, dControl1Data, dControl2Data, pControlData, precharge1Data, precharge2Data)
    
    @classmethod
    def GetPayloadFromBytes(cls, payloadBytes : bytearray) -> ConverterLiveDataPayload(Payload):
        return ConverterLiveDataPayload(*cls.ParseBytes(payloadBytes))