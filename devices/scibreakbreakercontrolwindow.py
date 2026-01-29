import tkinter as tk
import json

from graphical.canvaslineclass import *
from graphical.canvasrectangleclass import *
from graphical.canvastextclass import *
from graphical.canvascontrolswitch import *

from generic.genericconfignotebook import *

# this creates a subwindow for controlling a breaker
class SciBreakBreakerControlWindow(tk.Toplevel):
    def __init__(self, parent, breakerDevice, config):
        # store parameters
        super().__init__()
        self.breakerDevice = breakerDevice
        self.config = config
        self.wm_protocol('WM_DELETE_WINDOW', self.OnSubwindowDestroyCallback)
        self.title(self.breakerDevice.deviceName)
        
        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.grid(row=0, column=0)
        
        self.notebookFrame = tk.Frame(self)
        self.notebookFrame.grid(row=0, column=1, sticky="n")
        
        # load in graphical data
        self.graphicalElements = {}
        self.LoadGraphicalElements()
        
        # create a notebook to show the config
        self._CreateNotebook()
    
    def UpdateData(self, data, online, closed):
        # fill in new data
        print ("Updating breaker data")
        
        # voltages and currents
        if online:
            self.graphicalElements["voltageTop"].SetText(str(data.voltageTop) + " V")
            self.graphicalElements["voltageBot"].SetText(str(data.voltageBot) + " V")
            self.graphicalElements["currentTop"].SetText(str(data.currentTop) + " A")
            self.graphicalElements["currentBot"].SetText(str(data.currentBot) + " A")
        else:
            self.graphicalElements["voltageTop"].SetText("---" + " V")
            self.graphicalElements["voltageBot"].SetText("---" + " V")
            self.graphicalElements["currentTop"].SetText("---" + " A")
            self.graphicalElements["currentBot"].SetText("---" + " A")
        
        # online or not
        if online:
            t = self.notebook.GetElement("General:status")
            if t:
                t["text"] = "online"
        else:
            t = self.notebook.GetElement("General:status")
            if t:
                t["text"] = "offline"
        
        # setpoints of breakers
        self.tripLevelNotebook.GetElement("Trip Level:setpoint_top")["text"] = str(data.tripLevelTop)
        self.tripLevelNotebook.GetElement("Trip Level:setpoint_bot")["text"] = str(data.tripLevelBot)
        
        # switch representation
        sw = self.graphicalElements["switchTop"]
        if closed[0]:
            sw.Close(True)
        else:
            sw.Close(False)
        
        sw = self.graphicalElements["switchBot"]
        if closed[1]:
            sw.Close(True)
        else:
            sw.Close(False)
        
        # rest of status bits
        status = data.status
        displayString = ""
        
        if status & 0x0200:
            displayString += "Top breaker failure\n"
        
        if status & 0x0400:
            displayString += "Top breaker blocked\n"
        
        if status & 0x0800:
            displayString += "Top breaker ready\n"
        
        if status & 0x020000:
            displayString += "Bottom breaker failure\n"
        
        if status & 0x040000:
            displayString += "Bottom breaker blocked\n"
        
        if status & 0x080000:
            displayString += "Bottom breaker ready\n"
        
        # write
        textbox = self.statusNotebook.elementDict["Status:status"]
        textbox.delete(1.0, tk.END)
        textbox.insert(tk.END, displayString)
        
        return
    
    def LoadGraphicalElements(self):
        # open template filename
        with open("templates/breakercontrol.json", 'r') as f:
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
        self.breakerDevice.sciBreakBreakerControlWindow = None
        self.destroy()
        return
    
    def _CreateNotebook(self):
        # use one of the generic control features to fill the notebook with data
        notebookConfig = {}
        controlNotebookConfig = {}
        tripLevelNotebookConfig = {}
        
        # some general information
        generalConfig = {}
        generalConfig["name"] = CreateNotebookTextViewConfig(name="Breaker Name", value=self.config["name"])
        generalConfig["ip"] = CreateNotebookTextViewConfig(name="Breaker IP", value=self.config["ip"])
        generalConfig["port"] = CreateNotebookTextViewConfig(name="Breaker Port", value=self.config["port"])
        generalConfig["livedata"] = CreateNotebookCheckboxConfig(name="Receive live data", init="off", command=self._LiveDataCallback)
        generalConfig["status"] = CreateNotebookTextViewConfig(name="Device status", value="offline")
        
        notebookConfig["General"] = generalConfig
        
        # create the notebook
        self.notebook = GenericConfigNotebook(self.notebookFrame, notebookConfig)
        self.notebook.grid(row=0, column=1, sticky="new", padx=20, pady=20)
        
        # control notebook
        controlConfig = {}
        controlConfig["turn_on"] = CreateNotebookButtonConfig(label="Turn On", command=lambda: self.breakerDevice.SendTurnOnCommand(True))
        controlConfig["turn_off"] = CreateNotebookButtonConfig(label="Turn Off", command=lambda: self.breakerDevice.SendTurnOnCommand(False))
        controlConfig["close"] = CreateNotebookButtonConfig(label="Close", command=lambda: self.breakerDevice.SendSwitchCommand(True))
        controlConfig["open"]  = CreateNotebookButtonConfig(label="Open" , command=lambda: self.breakerDevice.SendSwitchCommand(False))
        
        controlNotebookConfig["Control"] = controlConfig
        
        # create
        self.controlNotebook = GenericConfigNotebook(self.notebookFrame, controlNotebookConfig)
        self.controlNotebook.grid(row=1, column=1, sticky="new", padx=20, pady=20)
        
        # setpoint notebook
        tripLevelControl = {}
        tripLevelControl["voltage"] = CreateNotebookTextEntryConfig(name="Trip Level", init="0")
        tripLevelControl["setmode"] = CreateNotebookButtonConfig(label="Set Trip Level", command=self._OnTripLevelChange)
        tripLevelControl["setpoint_top"] = CreateNotebookTextViewConfig(name="Setpoint Top", value=0)
        tripLevelControl["setpoint_bot"] = CreateNotebookTextViewConfig(name="Setpoint Bot", value=0)
        
        tripLevelNotebookConfig["Trip Level"] = tripLevelControl
        
        # create
        self.tripLevelNotebook = GenericConfigNotebook(self.notebookFrame, tripLevelNotebookConfig)
        self.tripLevelNotebook.grid(row=2, column=1, sticky="new", padx=20, pady=20)
        
        # status view
        statusView = {}
        statusView["status"] = CreateNotebookTextboxConfig(height=8)
        
        statusViewConfig = {}
        statusViewConfig["Status"] = statusView
        
        self.statusNotebook = GenericConfigNotebook(self.notebookFrame, statusViewConfig)
        self.statusNotebook.grid(row=3, column=1, sticky="new", padx=20, pady=20)
        
        return
    
    def _OnTripLevelChange(self):
        # get input element
        tripLevelEntry = self.tripLevelNotebook.GetElement("Trip Level:voltage")
        
        tripLevel = int(tripLevelEntry.get())
        
        self.breakerDevice.SendSetTripLevelCommand(tripLevel)
        
        return
    
    def _LiveDataCallback(self):
        # print
        box = self.notebook.GetElement("General:livedata")
        
        self.breakerDevice.SendLiveDataCommand(box.get() == 1)
        
        return
    
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
        text = CanvasText(self.canvas, 400, 400, config, 0)
        
        self.graphicalElements[key] = text
        
        return
    
    def _AppendControlSwitchElement(self, key, config):
        # create a new control switch
        switch = CanvasControlSwitch(self.canvas, 400, 400, config, 0, self)
        
        self.graphicalElements[key] = switch
        
        return