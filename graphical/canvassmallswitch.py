from graphical.canvaselementclass import *
from graphical.smallswitchrenderer import *

class CanvasSmallSwitch(CanvasElement):
    def __init__(self, canvas, baseX, baseY, config, rotation, root):
        # call init of superior class
        super().__init__(canvas, baseX, baseY)
        
        # setup other parameters
        self.posX = config["positionX"]
        self.posY = config["positionY"]
        self.rotation = 0
        initRotation = config["rotation"] + rotation
        normalColor = config["normalColor"]
        selectedColor = config["selectedColor"]
        
        # limit rotation
        while initRotation >= 360:
            initRotation -= 360
        
        while initRotation < 0:
            initRotation += 360
        
        # generate new image
        self.switch = SmallSchematicSwitch(root, self.canvas, self.posX + self.baseX, self.posY + self.baseY, 0, normalColor, selectedColor)
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        self.switch.SetBackgroundColor(config["backgroundColor"])
        
        # rotate image
        steps = int(initRotation / 90)
        for i in range(steps):
            self.RotateCW()
        
    def Update(self):
        self.switch.Update()
        return
    
    def Redraw(self):
        self.switch.Redraw()
        return
    
    def Delete(self):
        self.switch.Delete()
        return
    
    def Select(self, onOff):
        self.switch.SetSelected(onOff)
        return
    
    def Close(self, closed):
        self.switch.SetClosed(closed)
        return
    
    def Flip(self):
        # invert x axis position
        self.posX = -self.posX
        
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        
        return
    
    def RotateCW(self):
        self.rotation += 90
        while self.rotation >= 360:
            self.rotation -= 360
        
        self.switch.SetRotation(self.rotation)
        
        self.posX, self.posY = self.RotateCoordsCW(self.posX, self.posY)
        
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        
        return
    
    def RotateCCW(self):
        self.rotation -= 90
        while self.rotation < 0:
            self.rotation += 360
        
        self.switch.SetRotation(self.rotation)
        
        self.posX, self.posY = self.RotateCoordsCCW(self.posX, self.posY)
        
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        
        return
    
    def Move(self, posX, posY):
        super().Move(posX, posY)
        
        self.switch.SetToPosition(self.posX + self.baseX, self.posY + self.baseY)
        
        return