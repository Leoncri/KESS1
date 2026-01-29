class CanvasElement:
    def __init__(self, canvas, baseX, baseY):
        # store variables
        self.canvas = canvas
        self.baseX = baseX
        self.baseY = baseY
        
        self.isSelected = False
    
    def Update(self):
        # update the graphics of this element
        return
    
    def Redraw(self):
        # redraw this element
        return
    
    def Delete(self):
        # clears elements from canvas
        return
    
    def Select(self, onOff):
        # shows the element as selected
        return
    
    def Flip(self):
        # flips the element horizontally (on Y-axis)
        return
    
    def RotateCW(self):
        # rotate by 90 deg
        return
    
    def RotateCCW(self):
        # rotate by 90 deg
        return
    
    def MoveInit(self):
        # initializes a move
        return
    
    def Move(self, dX, dY):
        # move by a specific amount
        self.baseX += dX
        self.baseY += dY
    
    def MoveExit(self):
        # exists a move operation
        return
    
    def RotateCoordsCW(self, x, y):
        # rotate by 90 deg        
        return -y, x
    
    def RotateCoordsCCW(self, x, y):
        # rotate by -90 deg
        return y, -x