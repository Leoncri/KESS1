from graphical.canvaselementclass import *
from graphical.largeswitchrenderer import *

class CanvasControlSwitch(CanvasElement):
    def __init__(self, canvas, baseX, baseY, config, rotation, root):
        # call init of superior class
        super().__init__(canvas, baseX, baseY)
        
        # setup other parameters
        self.posX = config["positionX"]
        self.posY = config["positionY"]
        self.rotation = config["rotation"] + rotation
        lineOnColor = config["lineOnColor"]
        lineOffColor = config["lineOffColor"]
        
        # limit rotation
        while self.rotation >= 360:
            self.rotation -= 360
        
        while self.rotation < 0:
            self.rotation += 360
        
        # generate new image
        self.switch = LargeControlSwitch(root, self.canvas, self.posX + self.baseX, self.posY + self.baseY, self.rotation, lineOffColor, lineOnColor)
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        self.switch.SetBackgroundColor(config["backgroundColor"])
        
        
    
    def Update(self):
        self.switch.Update()
        return
    
    def Redraw(self):
        self.switch.Redraw()
        return
    
    def Delete(self):
        self.switch.Delete()
        return
    
    def Close(self, closed):
        self.switch.SetClosed(closed)
        return
    
    def SetOnClickCallback(self, callback):
        self.switch.extOnClickCallback = callback
        return