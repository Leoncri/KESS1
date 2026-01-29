import tkinter as tk
import tkinter.messagebox

class GenericConfigurationWindow(tk.Toplevel):
    def __init__(self, parent, config, onSaveCallback):
        # init parent
        super().__init__()
        
        # store variables
        self.config = config
        self.onSaveCallback = onSaveCallback
        
        # frame for adding the inputs to
        self.inputFrame = tk.Frame(self)
        self.buttonFrame = tk.Frame(self)
        
        # variables for storing the input values
        self.userInputs = []
        self.userInputValues = {}
        
        # start creating graphical elements
        for e in self.config:
            # create elements depending on type of config
            c = self.config[e]
            if c["type"] == "text":
                self._GenerateTextEntry(e, c["init"])
            elif c["type"] == "ip":
                self._GenerateTextEntry(e, c["init"])
            elif c["type"] == "int":
                self._GenerateTextEntry(e, c["init"])
        
        # create the user buttons
        self.buttonOK = tk.Button(self.buttonFrame, text="OK", command=self.OnButtonOK).grid(row=0, column=0)
        self.buttonSave = tk.Button(self.buttonFrame, text="Save", command=self.OnButtonSave).grid(row=0, column=1)
        self.buttonCheck = tk.Button(self.buttonFrame, text="Check", command=self.OnButtonCheck).grid(row=0, column=2)
        self.buttonCancel = tk.Button(self.buttonFrame, text="Cancel", command=self.OnButtonCancel).grid(row=0, column=3)
        
        # pack the frames to the main window
        self.inputFrame.grid(row=0, column=0)
        self.buttonFrame.grid(row=1, column=0)
    
    def OnButtonOK(self) -> None:
        # first save all variables
        self.OnButtonSave()
        
        # call the callback function for storing variables
        self.onSaveCallback(self.userInputValues)
        
        # close this window
        self.destroy()
    
    def OnButtonSave(self) -> None:
        # run over all variables and store them if needed
        for e in self.userInputs:
            key = e[0]
            var = e[1]
            
            c = self.config[key]
            
            if c["type"] == "text":
                self._SaveTextVariable(key, var)
            elif c["type"] == "ip":
                self._SaveIPVariable(key, var)
            elif c["type"] == "int":
                self._SaveIntegerVariable(key, var)
        
        return
    
    def OnButtonCheck(self) -> None:
        # check user inputs against contraints
        result = True
        for e in self.userInputs:
            # extract key and variable
            key = e[0]
            var = e[1]
            c = self.config[key]
            
            if c["type"] == "text":
                result &= self._CheckTextField(key, var)
            elif c["type"] == "ip":
                result &= self._CheckIPField(key, var)
            elif c["type"] == "int":
                result &= self._CheckIntegerField(key, var)
        
        if result:
            # present an success message
            tkinter.messagebox.showinfo(title="Input Check", message="All inputs were set correctly")
            
        return
    
    def OnButtonCancel(self) -> None:
        # call callback and return
        if self.userInputValues != {}:
            self.onSaveCallback(self.userInputValues)
        
        self.destroy()
    
    # this function generates a generic text entry field, used for text, integers, ...
    def _GenerateTextEntry(self, key, initValue) -> None:
        # generate a label to present the variable name
        name = str(key) + " :"
        row = len(self.userInputs)
        
        tk.Label(self.inputFrame, text=name).grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)
        
        # and the entry field
        self.userInputs.append([key, tk.StringVar(value=str(initValue))])
        tk.Entry(self.inputFrame, textvariable=self.userInputs[row][1]).grid(row=row, column=1, sticky=tk.E, padx=5, pady=5)
        
        return
    
    def _CheckTextField(self, key, var) -> bool:
        # get the maximum length and check against the variable content
        config = self.config[key]
        maxLen = config["maxLength"]
        text = var.get()
        
        if len(text) > maxLen:
            # show error field
            message = str(key) + " input field is to long (max: " + str(maxLen) + ")"
            tkinter.messagebox.showerror(title="Text entry error", message=message)
            return False
        
        return True
    
    def _CheckIPField(self, key, var) -> bool:
        # check the address
        if not self.__CheckIPAddress(var.get()):
            # show error message
            message = str(key) + " input field cannot be converted to IP address"
            tkinter.messagebox.showerror(title="IP entry error", message=message)
            return False
        
        return True
    
    def __CheckIPAddress(self, ipAddress) -> bool:
        if ipAddress == "localhost":
            return True
        octettsString = ipAddress.split(".")
        if len(octettsString) != 4:
            return False
        try:
            octetts = list(map(int, octettsString))
        except:
            return False
        for octett in octetts:
            if octett < 0 or octett > 255:
                return False
        return True
    
    def _CheckIntegerField(self, key, var) -> bool:
        # get min and max
        config = self.config[key]
        minValue = config["min"]
        maxValue = config["max"]
        
        try:
            value = int(var.get())
        except:
            # show error message
            message = str(key) + " cannot be converted to integer"
            tkinter.messagebox.showerror(title="Integer entry error", message=message)
            return False
        
        # check values
        if value < minValue or value > maxValue:
            # show error message
            message = str(key) + " is out of range (min: " + str(minValue) + ", max: " + str(maxValue) + ")"
            tkinter.messagebox.showerror(title="Integer entry error", message=message)
            return False
        
        return True
    
    def _SaveTextVariable(self, key, var):
        # check variable first
        if not self._CheckTextField(key, var):
            # show error message
            message = "Check of variable " + str(key) + " failed, resetting to default value"
            tkinter.messagebox.showwarning(title="Text entry error", message=message)
            self.userInputValues[key] = self.config[key]["init"]
        else:
            # just store the value
            self.userInputValues[key] = var.get()
        
        return
    
    def _SaveIPVariable(self, key, var):
        # check variable first
        if not self._CheckIPField(key, var):
            # show error message
            message = "Check of variable " + str(key) + " failed, resetting to default value"
            tkinter.messagebox.showwarning(title="IP entry error", message=message)
            self.userInputValues[key] = self.config[key]["init"]
        else:
            # just store the value
            self.userInputValues[key] = var.get()
        
        return
    
    def _SaveIntegerVariable(self, key, var):
        # check variable first
        if not self._CheckIntegerField(key, var):
            # show error message
            message = "Check of variable " + str(key) + " failed, resetting to default value"
            tkinter.messagebox.showwarning(title="Integer entry error", message=message)
            self.userInputValues[key] = self.config[key]["init"]
        else:
            # just store the value
            self.userInputValues[key] = int(var.get())
        
        return