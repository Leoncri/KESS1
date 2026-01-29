from tkinter import *
from tkinter.ttk import *
from auxillary.updateentry import *

def CreateNotebookTextViewConfig(name="", value=""):
    return {"type" : "textView", "name" : name, "value" : value}

def CreateNotebookCheckboxConfig(name="", init="off", command=None):
    return {"type" : "checkbox", "name" : name, "command" : command}

def CreateNotebookTextEntryConfig(name="", init=""):
    return {"type" : "textEntry", "name" : name, "init" : init}

def CreateNotebookDropDownConfig(name="", init="", choices=[]):
    return {"type" : "dropDown", "name" : name, "init" : init, "choices" : choices}

def CreateNotebookButtonConfig(label="", command=None):
    return {"type" : "button", "label" : label, "command" : command}

def CreateNotebookTextboxConfig(height=2, init=""):
    return {"type" : "textbox", "height" : height, "init" : init}

class GenericConfigNotebook(Notebook):
    def __init__(self, parent, notebookConfig):
        super().__init__(parent)
        
        # store config and start creating stuff
        self.config = notebookConfig
        
        # dictionary of created elements
        self.elementDict = {}
        
        self._CreateTabs()
    
    def GetElement(self, name):
        try:
            return self.elementDict[name]
        except:
            pass
        return None
    
    def SetWidth(self, size):
        return
    
    def _CreateTabs(self):
        # first create the tabs
        for e in self.config:
            # the key gives the tabs name
            # create a new frame to bundle all elements
            frame = Frame(self)
            self._CreateControls(frame, self.config[e], e)
            
            self.add(frame, text=e)
            self.tab(frame, sticky="ew")
        
        return
    
    def _CreateControls(self, frame, config, key):
        # create the controls for a specific tab
        rowCounter = 0
        for e in config:
            element = config[e]
            
            type = element["type"]
            
            if type == "textView":
                self.elementDict[key + ':' + e] = self._CreateTextView(frame, element, rowCounter)
            elif type == "checkbox":
                self.elementDict[key + ':' + e] = self._CreateCheckbox(frame, element, rowCounter)
            elif type == "textEntry":
                self.elementDict[key + ':' + e] = self._CreateTextEntry(frame, element, rowCounter)
            elif type == "dropDown":
                self.elementDict[key + ':' + e] = self._CreateDropDown(frame, element, rowCounter)
            elif type == "button":
                self.elementDict[key + ':' + e] = self._CreateButton(frame, element, rowCounter)
            elif type == "textbox":
                self.elementDict[key + ':' + e] = self._CreateTextbox(frame, element, rowCounter)
            
            rowCounter += 1
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        return
    
    def _CreateTextView(self, frame, config, row):
        # create a new text view
        name = config["name"]
        value = config["value"]
        
        nameLabel = Label(frame, text=(name + " :"))
        valueLabel = Label(frame, text=value)
        
        nameLabel.grid(row=row, column=0, sticky="e", padx=5)
        valueLabel.grid(row=row, column=1, sticky="w", padx=5)
        
        return valueLabel
    
    def _CreateCheckbox(self, frame, config, row):
        # create a new checkbox
        name = config["name"]
        var = IntVar()
        command = config["command"]
        
        nameLabel = Label(frame, text=(name + " :"))
        checkbox = Checkbutton(frame, variable=var, command=command)
        
        nameLabel.grid(row=row, column=0, sticky="e", padx=5)
        checkbox.grid(row=row, column=1, sticky="w", padx=5)
        
        return var
    
    def _CreateTextEntry(self, frame, config, row):
        # create the left side
        name = config["name"]
        nameLabel = Label(frame, text=(name + " :"))
        nameLabel.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        
        # create the string var
        sv = StringVar(frame)
        
        # create entry
        init = config["init"]
        entryBox = UpdateEntry(frame, text=init, textvariable=sv)
        entryBox.grid(row=row, column=1, sticky="e", padx=5, pady=2)
        
        return entryBox
    
    def _CreateTextbox(self, frame, config, row):
        # the textview spans both columns
        textBox = Text(frame, height=config["height"], width=25)
        textBox.insert(END, config["init"])
        
        textBox.grid(row=row, column=0, sticky="ew", columnspan=2, padx=2, pady=2)
        
        return textBox
    
    def _CreateDropDown(self, frame, config, row):
        # create the label
        name = config["name"]
        nameLabel = Label(frame, text=(name + " :"))
        nameLabel.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        
        # create drop down
        init = config["init"]
        choices = config["choices"]
        dropDown = Combobox(frame, state="readonly", values=choices)
        dropDown.set(init)
        dropDown.grid(row=row, column=1, sticky="e", padx=5, pady=2)
        
        return dropDown
    
    def _CreateButton(self, frame, config, row):
        # button spans two columns
        label = config["label"]
        command = config["command"]
        button = Button(frame, text=label, command=command)
        button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        return None