from tkinter import *
from genericconfigwindowclass import *

window = Tk()

# create a new config
ipConfig = {}
ipConfig["type"] = "ip"
ipConfig["init"] = "localhost"
portConfig = {}
portConfig["type"] = "int"
portConfig["init"] = 502
portConfig["min"] = 0
portConfig["max"] = 65535
config = {}
config["IP"] = ipConfig
config["Port"] = portConfig

def PrintReturnValues(values):
    print (values["IP"])
    print (values["Port"])

def CreateConfigWindow():
    c = GenericConfigurationWindow(window, config, PrintReturnValues)
    c.wait_window()
    return

# create new config window
b = Button(window, text="Config", command=CreateConfigWindow).pack()

window.mainloop()