import tkinter as tk
import json

from graphical.canvaslineclass import *
from graphical.canvasrectangleclass import *
from graphical.canvastextclass import *
from graphical.canvascontrolswitch import *

from generic.genericconfignotebook import *

from network.headers.convertercommand import *
from network.payloads.converterrespond import *

from scope.scopemanager import *

from auxillary.powerconversion import *

def CalculatePower(v1, c1, type1, v2, c2, type2):
    # if type ends with ac, calculate with sqrt(3) * v1 * v2
    try:
        if type1[-2:].lower() == "ac":
            p1 = v1 * c1 * 1.732
        else:
            p1 = v1 * c1
    except:
        p1 = v1 * c1
    
    try:
        if type2[-2:].lower() == "ac":
            p2 = v2 * c2 * 1.732
        else:
            p2 = v2 * c2
    except:
        p2 = v2 * c2
    
    return (p1 + p2) / 2

# this creates a subwindow for controlling a converter
class ConverterControlWindow(tk.Toplevel):
    def __init__(self, parent, converterDevice, config, scopeManager):
        # store parameters
        super().__init__()
        self.converterDevice = converterDevice
        self.scopeManager = scopeManager
        self.config = config
        self.wm_protocol('WM_DELETE_WINDOW', self.OnSubwindowDestroyCallback)
        self.title(self.converterDevice.deviceName)
        
        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.grid(row=0, column=0, sticky="n")
        
        self.notebookFrame = tk.Frame(self)
        self.notebookFrame.grid(row=0, column=1)
        
        self.notebookViewFrame = tk.Frame(self)
        self.notebookViewFrame.grid(row=0, column=2)
        
        # load in graphical data
        self.graphicalElements = {}
        self.LoadGraphicalElements()
        self.graphicalElements["Side1Type"].SetText(self.converterDevice.port1Type[-2:])
        self.graphicalElements["Side2Type"].SetText(self.converterDevice.port2Type[-2:])
        
        # create a notebook to show the config
        self._CreateNotebook()
    
    def Update(self, Data):
        # update voltage and current values
        v1 = Data.voltageMeasurement.voltageP1 + Data.voltageMeasurement.voltageM1
        v2 = Data.voltageMeasurement.voltageP2 + Data.voltageMeasurement.voltageM2
        self.graphicalElements["Side1Voltage"].SetText(str(v1) + " V")
        self.graphicalElements["Side2Voltage"].SetText(str(v2) + " V")
        
        if Data.currentMeasurement.currentM1 < 100:
            c1 = Data.currentMeasurement.currentP1
        else:
            c1 = (Data.currentMeasurement.currentP1 + Data.currentMeasurement.currentM1) / 2
        
        if Data.currentMeasurement.currentM2 < 100:
            c2 = Data.currentMeasurement.currentP2
        else:
            c2 = (Data.currentMeasurement.currentP2 + Data.currentMeasurement.currentM2) / 2
        
        self.graphicalElements["Side1Current"].SetText(str(c1) + " A")
        self.graphicalElements["Side2Current"].SetText(str(c2) + " A")
        
        # update generic values
        try:
            # operating mode
            self.generalNotebook.elementDict["General:opmode"]['text'] = ConverterModeNames.names[Data.statusDataSet.mode]
            
            # power
            power = CalculatePower(v1, c1, self.converterDevice.port1Type, v2, c2, self.converterDevice.port2Type) / 1000
            #power = int((v1 * c1 + v2 * c2) / 2000)
            print("Power value: " + str(Data.staticDataSet.power))
            maxPower = int(ParsePowerValue(Data.staticDataSet.power) / 1000)
            percent = int(abs(power / maxPower) * 100)
            self.generalNotebook.elementDict["General:power"]['text'] = str(round(power, 2)) + " kW (" + str(percent) + " %)"
            
            if power > 0:
                if self.converterDevice.graphicalElementHandler.rotation in [0, 270]:
                    self.converterDevice.graphicalElementHandler.graphicalElementsDict["Power"].SetText(str(round(power, 2)) + " kW >>")
                else:
                    self.converterDevice.graphicalElementHandler.graphicalElementsDict["Power"].SetText("<< " + str(round(power, 2)) + "kW")
            
            elif power == 0:
                self.converterDevice.graphicalElementHandler.graphicalElementsDict["Power"].SetText("< 0 kW >")
            
            else:
                if self.converterDevice.graphicalElementHandler.rotation in [90, 180]:
                    self.converterDevice.graphicalElementHandler.graphicalElementsDict["Power"].SetText(str(round(power, 2)) + " kW >>")
                else:
                    self.converterDevice.graphicalElementHandler.graphicalElementsDict["Power"].SetText("<< " + str(round(power, 2)) + "kW")
                
        except Exception as e:
            print (e)
        
        # update voltage setpoints
        self.voltageNotebook.elementDict["Voltage Control Side 1:voltage"].SetText(str(Data.voltageControl1Data.voltage))
        self.voltageNotebook.elementDict["Voltage Control Side 2:voltage"].SetText(str(Data.voltageControl2Data.voltage))
        
        # update power control
        self.powerNotebook.elementDict["Power:power"].SetText(str(Data.powerControlData.power))
        
        # update status, warnings and errors
        try:
            status = Data.statusDataSet.state
            textbox = self.statusNotebook.elementDict["Status:status"]
            textbox.delete(1.0, tk.END)
            for i in range(16):
                if status & (1 << i):
                    # add text to box
                    textbox.insert(tk.END, ConverterStatusNames.names[i])
            
            warnings = Data.statusDataSet.warnings
            textbox = self.warningsNotebook.elementDict["Warnings:warnings"]
            textbox.delete(1.0, tk.END)
            for i in range(16):
                if warnings & (1 << i):
                    # add text to box
                    textbox.insert(tk.END, ConverterWarningMessages.Messages[i])
            
            errors = Data.statusDataSet.errors
            textbox = self.errorsNotebook.elementDict["Errors:errors"]
            textbox.delete(1.0, tk.END)
            for i in range(16):
                if errors & (1 << i):
                    # add text to box
                    textbox.insert(tk.END, ConverterErrorMessages.Messages[i])
            
        except Exception as e:
            print (e)
        
        return
    
    def LoadGraphicalElements(self):
        # open template filename
        with open("templates/convertercontrol.json", 'r') as f:
            config = json.load(f)
        
        graphical = config["graphical"]
        
        for e in graphical:
            element = graphical[e]
            type = element["type"]
            
            if type == "line":
                self._AppendLineElement(e, element)
            elif type == "rectangle":
                self._AppendRectangleElement(e, element)
            elif type == "text":
                self._AppendTextElement(e, element)
            elif type == "controlSwitch":
                self._AppendControlSwitchElement(e, element)
        
        return
    
    def OnSubwindowDestroyCallback(self):
        self.converterDevice.converterControlWindow = None
        self.destroy()
        return
    
    def _CreateNotebook(self):
        # use one of the generic control features to fill the notebook with data
        notebookConfig = {}
        
        # some general information
        generalConfig = {}
        generalConfig["name"] = CreateNotebookTextViewConfig(name="Converter Name", value=self.config["name"])
        generalConfig["ip"] = CreateNotebookTextViewConfig(name="Converter IP", value=self.config["ip"])
        generalConfig["port"] = CreateNotebookTextViewConfig(name="Converter Port", value=self.config["port"])
        generalConfig["livedata"] = CreateNotebookCheckboxConfig(name="Receive live data", init="off", command=self._LiveDataCallback)
        generalConfig["status"] = CreateNotebookTextViewConfig(name="Device status", value="offline")
        generalConfig["opmode"] = CreateNotebookTextViewConfig(name="Operating Mode", value="OFF")
        generalConfig["power"] = CreateNotebookTextViewConfig(name="Power", value="0 kW (0%)")
        generalConfig["offButton"] = CreateNotebookButtonConfig(label="OFF", command=self._OnConverterOff)
        generalConfig["idleButton"] = CreateNotebookButtonConfig(label="IDLE", command=self._OnConverterIdle)
        generalConfig["resetButton"] = CreateNotebookButtonConfig(label="RESET", command=self._OnConverterReset)
        
        notebookConfig["General"] = generalConfig
        
        # create the notebook for general data
        self.generalNotebook = GenericConfigNotebook(self.notebookFrame, notebookConfig)
        self.generalNotebook.grid(row=0, column=0, sticky="ew", padx=0, pady=20)
        
        # precharge data
        prechargeChoices = ["Voltage Control", "Droop Control"]
        precharge1Data = {}
        precharge1Data["nextmode"] = CreateNotebookDropDownConfig(name="Next Mode", init="Voltage Control", choices=prechargeChoices)
        precharge1Data["setmode"] = CreateNotebookButtonConfig(label="Precharge", command=lambda: self._OnPrecharge(1))
        
        precharge2Data = {}
        precharge2Data["nextmode"] = CreateNotebookDropDownConfig(name="Next Mode", init="Voltage Control", choices=prechargeChoices)
        precharge2Data["setmode"] = CreateNotebookButtonConfig(label="Precharge", command=lambda: self._OnPrecharge(2))
        
        prechargeConfig = {}
        prechargeConfig["Precharge Side 1"] = precharge1Data
        prechargeConfig["Precharge Side 2"] = precharge2Data
        
        # create the notebook for precharge data
        self.prechargeNotebook = GenericConfigNotebook(self.notebookFrame, prechargeConfig)
        self.prechargeNotebook.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        
        # voltage control
        voltage1Control = {}
        voltage1Control["voltage"] = CreateNotebookTextEntryConfig(name="Voltage", init="0")
        voltage1Control["setmode"] = CreateNotebookButtonConfig(label="Voltage Control", command=lambda: self._OnVoltageControl(1))
        
        voltage2Control = {}
        voltage2Control["voltage"] = CreateNotebookTextEntryConfig(name="Voltage", init="0")
        voltage2Control["setmode"] = CreateNotebookButtonConfig(label="Voltage Control", command=lambda: self._OnVoltageControl(2))
        
        voltageControl = {}
        voltageControl["Voltage Control Side 1"] = voltage1Control
        voltageControl["Voltage Control Side 2"] = voltage2Control
        
        # create the notebook for voltage control data
        self.voltageNotebook = GenericConfigNotebook(self.notebookFrame, voltageControl)
        self.voltageNotebook.grid(row=2, column=0, sticky="ew", padx=0, pady=20)
        
        # droop control
        droop1Control = {}
        droop1Control["setmode"] = CreateNotebookButtonConfig(label="Droop Mode", command=lambda: self._OnDroopControl(1))
        
        droop2Control = {}
        droop2Control["setmode"] = CreateNotebookButtonConfig(label="Droop Mode", command=lambda: self._OnDroopControl(2))
        
        droopControl = {}
        droopControl["Droop Control Side 1"] = droop1Control
        droopControl["Droop Control Side 2"] = droop2Control
        
        # create the notebook for droop control
        self.droopNotebook = GenericConfigNotebook(self.notebookFrame, droopControl)
        self.droopNotebook.grid(row=3, column=0, sticky="ew", padx=0, pady=0)
        
        # power control
        powerControl = {}
        powerControl["power"] = CreateNotebookTextEntryConfig(name="Power 1 -> 2", init="0")
        powerControl["setmode"] = CreateNotebookButtonConfig(label="Power Control", command=self._OnPowerControl)
        
        powerConfig = {}
        powerConfig["Power"] = powerControl
        
        #create the notebook for power control
        self.powerNotebook = GenericConfigNotebook(self.notebookFrame, powerConfig)
        self.powerNotebook.grid(row=4, column=0, sticky="ew", padx=0, pady=20)
        
        # discharge control
        discharge1Control = {}
        discharge1Control["setmode"] = CreateNotebookButtonConfig(label="Discharge", command=lambda: self._OnDischarge(1))
        
        discharge2Control = {}
        discharge2Control["setmode"] = CreateNotebookButtonConfig(label="Discharge", command=lambda: self._OnDischarge(2))
        
        dischargeConfig = {}
        dischargeConfig["Discharge Side 1"] = discharge1Control
        dischargeConfig["Discharge Side 2"] = discharge2Control
        
        # create the notebook for discharge
        self.dischargeNotebook = GenericConfigNotebook(self.notebookFrame, dischargeConfig)
        self.dischargeNotebook.grid(row=5, column=0, sticky="ew", padx=0, pady=0)
        
        # notebooks for status, warnings and errors
        statusView = {}
        statusView["status"] = CreateNotebookTextboxConfig(height=5)
        
        statusViewConfig = {}
        statusViewConfig["Status"] = statusView
        
        self.statusNotebook = GenericConfigNotebook(self.notebookViewFrame, statusViewConfig)
        self.statusNotebook.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        warningsView = {}
        warningsView["warnings"] = CreateNotebookTextboxConfig(height=16)
        
        warningsViewConfig = {}
        warningsViewConfig["Warnings"] = warningsView
        
        self.warningsNotebook = GenericConfigNotebook(self.notebookViewFrame, warningsViewConfig)
        self.warningsNotebook.grid(row=1, column=0, sticky="ew", padx=20, pady=0)
        
        errorsView = {}
        errorsView["errors"] = CreateNotebookTextboxConfig(height=16)
        
        errorsViewConfig = {}
        errorsViewConfig["Errors"] = errorsView
        
        self.errorsNotebook = GenericConfigNotebook(self.notebookViewFrame, errorsViewConfig)
        self.errorsNotebook.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        
        # get width of notebooks
        self.generalNotebook.update()
        size = self.generalNotebook.winfo_width()
        self.generalNotebook.SetWidth(size)
        
        return
    
    def _LiveDataCallback(self):
        # get checkbox
        box = self.generalNotebook.GetElement("General:livedata")
        
        self.converterDevice.SendLiveDataCommand(box.get() == 1)
        return
    
    def _OnConverterOff(self):
        self.converterDevice.SendOffCommand()
        return
    
    def _OnConverterIdle(self):
        self.converterDevice.SendIdleCommand()
        return
    
    def _OnConverterReset(self):
        self.converterDevice.SendResetCommand()
        return
    
    def _OnPrecharge(self, side):
        print ("Precharge side " + str(side))
        dropDown = None
        if side == 1:
            # get drop down menu
            dropDown = self.prechargeNotebook.GetElement("Precharge Side 1:nextmode")
        elif side == 2:
            # get drop down menu
            dropDown = self.prechargeNotebook.GetElement("Precharge Side 2:nextmode")
        else:
            print ("Cannot get a dropdown element for precharge")
            return
        
        mode = dropDown.get()
        print ("Drop down mode is " + str(mode))
        if mode == "Voltage Control":
            if self._UpdateVoltageControlParameters(side):
                self.converterDevice.SendPrechargeCommand(side, mode="voltage")
        
        elif mode == "Droop Control":
            if self._UpdateDroopControlParameters(side):
                self.converterDevice.SendPrechargeCommand(side, mode="droop")
        return
    
    def _OnVoltageControl(self, side):
        print ("Voltage control side " + str(side))
        
        if self._UpdateVoltageControlParameters(side):
            self.converterDevice.SendVoltageControlCommand(side)
        
        if side == 1:
            self.voltageNotebook.elementDict["Voltage Control Side 1:voltage"].ResetChanged()
        else:
            self.voltageNotebook.elementDict["Voltage Control Side 2:voltage"].ResetChanged()
        
        return
    
    def _OnDroopControl(self, side):
        print ("Droop control side " + str(side))
        
        self.converterDevice.SendDroopControlCommand(side)
        
        return
    
    def _OnPowerControl(self):
        print ("Power control")
        
        # get power
        try:
            power = float(self.powerNotebook.elementDict["Power:power"].get().replace(',', '.'))
            power = max(min(power, 100), -100)
            pValue = int(power * 100) + 32768
        except Exception as e:
            print (e)
            return
        
        # set power
        if self.converterDevice.SendPowerControlParameter(pValue):
            self.converterDevice.SendPowerControlCommand()
        
        return
    
    def _OnDischarge(self, side):
        print ("Discharge side " + str(side))
        
        self.converterDevice.SendDischargeCommand(side)
        
        return
    
    def _UpdateVoltageControlParameters(self, side):
        voltageEntry = None
        if side == 1:
            # get voltage and update parameters for converter
            voltageEntry = self.voltageNotebook.GetElement("Voltage Control Side 1:voltage")
        
        elif side == 2:
            # get voltage and update parameters for converter
            voltageEntry = self.voltageNotebook.GetElement("Voltage Control Side 2:voltage")
        
        else:
            print ("Cannot get a voltage entry to update parameters from")
            return False
        
        try:
            voltage = int(voltageEntry.get())
            if voltage < 0:
                print ("Broken voltage in voltage setpoint")
                return False
        except Exception as e:
            print (e)
            return False
        
        print ("Send voltage control parameters")
        return self.converterDevice.SendVoltageControlParameters(side, voltage)
    
    # function to append a line
    def _AppendLineElement(self, key, config):
        # create a new line
        line = CanvasLine(self.canvas, 400, 400, config, 0)
        
        self.graphicalElements[key] = line
        
        return
    
    # function to append a rectangle
    def _AppendRectangleElement(self, key, config):
        # create a new rectangle
        rect = CanvasRectangle(self.canvas, 400, 400, config, 0)
        
        self.graphicalElements[key] = rect
        
        return
    
    def _AppendTextElement(self, key, config):
        # create a new text
        text = CanvasText(self.canvas, 400, 400, config, 0, scopeManager = self.scopeManager, name = self.converterDevice.deviceName + "-" + key)
        
        self.graphicalElements[key] = text
        
        return
    
    def _AppendControlSwitchElement(self, key, config):
        # create a new control switch
        switch = CanvasControlSwitch(self.canvas, 400, 400, config, 0, self)
        
        self.graphicalElements[key] = switch
        
        return