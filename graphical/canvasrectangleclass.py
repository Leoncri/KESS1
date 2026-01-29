from graphical.canvaselementclass import *

class CanvasRectangle(CanvasElement):
    def __init__(self, canvas, baseX, baseY, config, rotation):
        # init element
        super().__init__(canvas, baseX, baseY)
        
        # store rest of variables
        self.startX = config["startPositionX"]
        self.startY = config["startPositionY"]
        self.endX = config["endPositionX"]
        self.endY = config["endPositionY"]
        
        self.normalOutlineColor = config["normalOutlineColor"]
        self.normalFillColor = config["normalFillColor"]
        self.normalWidth = config["normalWidth"]
        self.selectedOutlineColor = config["selectedOutlineColor"]
        self.selectedFillColor = config["selectedFillColor"]
        self.selectedWidth = config["selectedWidth"]
        
        # rotate the rectangle
        steps = int(rotation / 90)
        for i in range(steps):
            self.startX, self.startY = self.RotateCoordsCW(self.startX, self.startY)
            self.endX, self.endY = self.RotateCoordsCW(self.endX, self.endY)
        
        # actual graphical element
        self.canvasRect = self.canvas.create_rectangle(self.startX + self.baseX, self.startY + self.baseY,
                                                        self.endX + self.baseX, self.endY + self.baseY,
                                                        outline=self.normalOutlineColor, fill=self.normalFillColor, width=self.normalWidth)
    
    def Update(self):
        # update rectangle on canvas
        self.canvas.coords(self.canvasRect, self.startX + self.baseX, self.startY + self.baseY, self.endX + self.baseX, self.endY + self.baseY)
        
        if self.isSelected:
            self.canvas.itemconfig(self.canvasRect, outline=self.selectedOutlineColor, fill=self.selectedFillColor, width=self.selectedWidth)
        else:
            self.canvas.itemconfig(self.canvasRect, outline=self.normalOutlineColor, fill=self.normalFillColor, width=self.normalWidth)
        
        return
    
    def Redraw(self):
        # delete rectangle from canvas
        self.canvas.delete(self.canvasRect)
        
        # create new rectangle
        self.canvasRect = self.canvas.create_rectangle(self.startX + self.baseX, self.startY + self.baseY,
                                                        self.endX + self.baseX, self.endY + self.baseY,
                                                        outline=self.normalOutlineColor, fill=self.normalFillColor, width=self.normalWidth)
        self.Update()
        
        return
    
    def Delete(self):
        # remove line from canvas
        if self.canvasRect:
            self.canvas.delete(self.canvasRect)
            self.canvasRect = None
        
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