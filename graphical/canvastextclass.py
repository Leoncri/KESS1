from graphical.canvaselementclass import *

class CanvasText(CanvasElement):
    def __init__(self, canvas, baseX, baseY, config, rotation, scopeManager = None, name = ""):
        # call element init
        super().__init__(canvas, baseX, baseY)
        
        # store rest of variables
        self.textX = config["textPositionX"]
        self.textY = config["textPositionY"]
        self.text = config["text"]
        self.textSize = config["size"]
        self.textFont = config["font"]
        self.rotation = config["rotation"]
        
        self.scopeManager = scopeManager
        self.name = name
        self.value = 0
        
        # text element
        self.canvasText = self.canvas.create_text(self.textX + self.baseX, self.textY + self.baseY, text=self.text, font = (self.textFont, self.textSize), angle = self.rotation)
        
        # set rotation
        steps = int(rotation / 90)
        for i in range(steps):
            self.RotateCW()
        
        # add a callback if this can be watched inside a scope
        if self.scopeManager:
            self.canvas.tag_bind(self.canvasText, "<Double-1>", self._OnScopeConfig)
    
    def Update(self):
        # update text on canvas
        self.canvas.coords(self.canvasText, self.textX + self.baseX, self.textY + self.baseY)
        self.canvas.itemconfig(self.canvasText, text=self.text, font = (self.textFont, self.textSize), angle = self.rotation)
    
    def SetText(self, text):
        self.text = text
        self.Update()
        return
    
    def SetValueUnit(self, value, unit):
        self.text = str(value) + " " + unit
        self.value = value
        self.Update()
        return
    
    def GetValue(self):
        return self.value
    
    # redraw the text
    def Redraw(self):
        # delete text from canvas
        self.canvas.delete(self.canvasText)
        
        # create new text on canvas
        self.canvasText = self.canvas.create_text(self.textX + self.baseX, self.textY + self.baseY, text=self.text, font = (self.textFont, self.textSize), angle = self.rotation)
        self.Update()
        
        return
    
    # remove text from canvas
    def Delete(self):
        if self.canvasText:
            self.canvas.delete(self.canvasText)
            self.canvasText = None
        
        return
    
    # flip the text
    def Flip(self):
        # invert x axis position
        self.textX = -self.textX
        
        # redraw
        self.Update()
        
        return
    
    # rotate text clockwise
    def RotateCW(self):
        # only rotate to 0 and 90 deg
        self.rotation += 90
        if self.rotation > 90:
            self.rotation -= 180

        # rotate the coords of the text
        self.textX, self.textY = self.RotateCoordsCW(self.textX, self.textY)
        
        # redraw
        self.Update()
        
        return
    
    # rotate text counterclockwise
    def RotateCCW(self):
        # only rotate to 90 and 0 deg
        self.rotation -= 90
        if self.rotation < 0:
            self.rotation += 180;
        
        # rotate the coords of the text
        self.textX, self.textY = self.RotateCoordsCCW(self.textX, self.textY)
        
        # redraw
        self.Update()
        
        return
    
    def Move(self, dX, dY):
        # call superior function
        super().Move(dX, dY)
        
        # redraw
        self.Update()
        
        return
    
    def _OnScopeConfig(self, event):
        # call scope manager
        if self.scopeManager:
            self.scopeManager.OpenConfigWindow(self, self.name)