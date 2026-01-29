from tkinter import *

class UpdateEntry(Entry):
    def __init__(self, root, text, textvariable):
        super().__init__(root, text=text, textvariable=textvariable)
        
        self.lastValue = ""
        self.hasFocus = False
        self.wasChanged = False
        
        # set bindings
        self.bind("<FocusIn>", self.OnFocusIn)
        self.bind("<FocusOut>", self.OnFocusOut)
        
        # store textvariable
        self.tvSave = textvariable
    
    def SetText(self, text):
        # check if text can be set
        if not self.hasFocus:
            if not self.wasChanged:
                self.delete(0,END)
                self.insert(0,text)
        
        return
    
    def OnFocusIn(self, event):
        # check which way focus goes
        self.hasFocus = True
        self.lastValue = self.tvSave.get()
        print ("Focus In")

        return
    
    def OnFocusOut(self, event):
        # Focus Out
        if self.lastValue != self.tvSave.get():
            self.wasChanged = True
            print ("Entry has changed")
        else:
            print ("Entry has not changed")
        self.hasFocus = False
        print ("Focus Out")
        
        return
    
    def ResetChanged(self):
        self.wasChanged = False
        return