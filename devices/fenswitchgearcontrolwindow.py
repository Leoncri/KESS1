import tkinter as tk
import json

from graphical.canvaslineclass import *
from graphical.canvasrectangleclass import *
from graphical.canvastextclass import *
from graphical.canvascontrolswitch import *

from generic.genericconfignotebook import *

# this creates a subwindow for controlling a switchgear
class SwitchgearControlWindow(tk.Toplevel):
    def __init__(self, parent, switchgearDevice, config):
        # store parameters
        super().__init__()
        self.switchgearDevice = switchgearDevice
        self.config = config
        self.wm_protocol('WM_DELETE_WINDOW', self.OnSubwindowDestroyCallback)
        self.title(self.switchgearDevice.deviceName)
        
        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.grid(row=0, column=0)
        
        # load in graphical data
        self.graphicalElements = {}
        self.LoadGraphicalElements()
        
        # setup callbacks for switches
        self.graphicalElements["Switch_1"].SetOnClickCallback(self._Switch1Callback)
        self.graphicalElements["Switch_2"].SetOnClickCallback(self._Switch2Callback)
        self.graphicalElements["Switch_3"].SetOnClickCallback(self._Switch3Callback)
        self.graphicalElements["Switch_4"].SetOnClickCallback(self._Switch4Callback)
        self.graphicalElements["Switch_5"].SetOnClickCallback(self._Switch5Callback)
        
        # create a notebook to show the config
        self._CreateNotebook()
        
    
    def UpdateData(self, data, online, closedSwitches):
        # fill in new data
        up, um, c1, c2, c3, c4 = data
        
        self.graphicalElements["Voltage_P"].SetText(str(up) + " V")
        self.graphicalElements["Voltage_M"].SetText(str(um) + " V")
        self.graphicalElements["Switch_1_Current"].SetText(str(c1) + " A")
        self.graphicalElements["Switch_2_Current"].SetText(str(c2) + " A")
        self.graphicalElements["Switch_3_Current"].SetText(str(c3) + " A")
        self.graphicalElements["Switch_4_Current"].SetText(str(c4) + " A")
        
        if online:
            t = self.notebook.GetElement("General:status")
            if t:
                t["text"] = "online"
        else:
            t = self.notebook.GetElement("General:status")
            if t:
                t["text"] = "offline"
        
        for i in range(5):
            # get switch
            tag = "Switch_" + str(i + 1)
            sw = self.graphicalElements[tag]
            if closedSwitches & (0x1 << i):
                sw.Close(True)
            else:
                sw.Close(False)
        
        return
    
    def LoadGraphicalElements(self):
        # open template filename
        with open("templates/fenswitchgearcontrol.json", 'r') as f:
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
        self.switchgearDevice.fenSwitchgearControlWindow = None
        self.destroy()
        return
    
    def _CreateNotebook(self):
        # use one of the generic control features to fill the notebook with data
        notebookConfig = {}
        
        # some general information
        generalConfig = {}
        generalConfig["name"] = CreateNotebookTextViewConfig(name="Switchgear Name", value=self.config["name"])
        generalConfig["ip"] = CreateNotebookTextViewConfig(name="Switchgear IP", value=self.config["ip"])
        generalConfig["port"] = CreateNotebookTextViewConfig(name="Switchgear Port", value=self.config["port"])
        generalConfig["livedata"] = CreateNotebookCheckboxConfig(name="Receive live data", init="off", command=self._LiveDataCallback)
        generalConfig["status"] = CreateNotebookTextViewConfig(name="Device status", value="offline")
        
        notebookConfig["General"] = generalConfig
        
        # create the notebook
        self.notebook = GenericConfigNotebook(self, notebookConfig)
        self.notebook.grid(row=0, column=1, sticky="nw", padx=20, pady=20)
        
        return
    
    def _Switch1Callback(self, closed):
        # call device to send command
        self.switchgearDevice.SendSwitchCommand(1, closed)
        return
    
    def _Switch2Callback(self, closed):
        # call device to send command
        self.switchgearDevice.SendSwitchCommand(2, closed)
        return
    
    def _Switch3Callback(self, closed):
        # call device to send command
        self.switchgearDevice.SendSwitchCommand(3, closed)
        return
    
    def _Switch4Callback(self, closed):
        # call device to send command
        self.switchgearDevice.SendSwitchCommand(4, closed)
        return
    
    def _Switch5Callback(self, closed):
        # call device to send command
        self.switchgearDevice.SendSwitchCommand(5, closed)
        return
    
    def _LiveDataCallback(self):
        # print
        box = self.notebook.GetElement("General:livedata")
        
        self.switchgearDevice.SendLiveDataCommand(box.get() == 1)
        
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