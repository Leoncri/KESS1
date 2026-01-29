from graphical.canvaselementclass import *

class CanvasLine(CanvasElement):
    def __init__(self, canvas, baseX, baseY, config, rotation):
        # call init of superior class
        super().__init__(canvas, baseX, baseY)
        
        # store rest of variables
        self.startX = config["startPositionX"]
        self.startY = config["startPositionY"]
        self.endX = config["endPositionX"]
        self.endY = config["endPositionY"]
        
        self.normalColor = config["normalColor"]
        self.normalWidth = config["normalWidth"]
        self.selectedColor = config["selectedColor"]
        self.selectedWidth = config["selectedWidth"]
        
        # rotate the line
        steps = int(rotation / 90)
        for i in range(steps):
            self.startX, self.startY = self.RotateCoordsCW(self.startX, self.startY)
            self.endX, self.endY = self.RotateCoordsCW(self.endX, self.endY)
        
        # actual graphical element
        self.canvasLine = self.canvas.create_line(self.startX + self.baseX, self.startY + self.baseY, self.endX + self.baseX, self.endY + self.baseY, fill=self.normalColor, width=self.normalWidth)
    
    def Update(self):
        # update the line on canvas
        self.canvas.coords(self.canvasLine, self.startX + self.baseX, self.startY + self.baseY, self.endX + self.baseX, self.endY + self.baseY)
        
        if self.isSelected:
            self.canvas.itemconfig(self.canvasLine, fill=self.selectedColor, width=self.selectedWidth)
        else:
            self.canvas.itemconfig(self.canvasLine, fill=self.normalColor, width=self.normalWidth)
        
        return
    
    def Redraw(self):
        # delete line from canvas
        self.canvas.delete(self.canvasLine)
        
        # create new line and update
        self.canvasLine = self.canvas.create_line(self.startX + self.baseX, self.startY + self.baseY, self.endX + self.baseX, self.endY + self.baseY, fill=self.normalColor, width=self.normalWidth)
        self.Update()
        
        return
    
    def Delete(self):
        # remove line from canvas
        if self.canvasLine:
            self.canvas.delete(self.canvasLine)
            self.canvasLine = None
        
        return
    
    def Select(self, onOff):
        # change color and width of line
        self.isSelected = onOff
        self.Update()
        
        return
    
    def Flip(self):
        # invert x axis positions
        self.startX = -self.startX
        self.endX = -self.endX
        
        # Redraw
        self.Update()
        
        return
    
    def RotateCW(self):
        # adjust actual X and Y coords
        self.startX, self.startY = self.RotateCoordsCW(self.startX, self.startY)
        
        self.endX, self.endY = self.RotateCoordsCW(self.endX, self.endY)
        
        # Redraw
        self.Update()
        
        return
    
    def RotateCCW(self):
        # adjust actual X and Y coords
        self.startX, self.startY = self.RotateCoordsCCW(self.startX, self.startY)
        
        self.endX, self.endY = self.RotateCoordsCCW(self.endX, self.endY)

        # Redraw
        self.Update()
        
        return
    
    def Move(self, dX, dY):
        # call superior function
        super().Move(dX, dY)
        
        # redraw
        self.Update()
        
        return