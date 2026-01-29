from graphical.canvaselementclass import *

class ConnectionPoint(CanvasElement):
    def __init__(self, canvas, baseX, baseY, connectionPoint, rotation):
        # call element init
        super().__init__(canvas, baseX, baseY)
        
        # store rest of variables
        self.posX = connectionPoint.posX - baseX
        self.posY = connectionPoint.posY - baseY
        self.type = connectionPoint.type
        self.connectionPoint = connectionPoint
        self.connectionPoint.SpreadType(self.type)
    
    # delete this connection
    def Delete(self):
        self.connectionPoint.ConnectionRemoved()
        self.connectionPoint = None
    
    # flip horizontally
    def Flip(self):
        # invert x axis position
        self.posX = -self.posX
        
        # call all three functions for the given point
        self.connectionPoint.OnPointMoveInit()
        self.connectionPoint.OnPointMove(2 * self.posX, 0)
        self.connectionPoint.OnPointMoveExit()
        
    # rotate the connection point clockwise
    def RotateCW(self):
        # rotate coords and notify connected point about move
        oldX = self.posX
        oldY = self.posY
        
        # rotate
        self.posX, self.posY = self.RotateCoordsCW(self.posX, self.posY)

        # calculate dX and dY and call point move functions
        dX = self.posX - oldX
        dY = self.posY - oldY
        
        # call all three functions for the given point
        self.connectionPoint.OnPointMoveInit()
        self.connectionPoint.OnPointMove(dX, dY)
        self.connectionPoint.OnPointMoveExit()
        
        return
    
    # rotate counterclockwise
    def RotateCCW(self):
        # rotate coords and notify connected point about move
        oldX = self.posX
        oldY = self.posY
        
        # rotate
        self.posX, self.posY = self.RotateCoordsCCW(self.posX, self.posY)
        
        # calculate dX and dY and call point move functions
        dX = self.posX - oldX
        dY = self.posY - oldY
        
        # call all three functions for the given point
        self.connectionPoint.OnPointMoveInit()
        self.connectionPoint.OnPointMove(dX, dY)
        self.connectionPoint.OnPointMoveExit()
        
        return
    
    def SwapConnectionPoint(self, new, keep=False):
        # notify old connection point
        self.connectionPoint.ConnectionRemoved(keep=keep)
        
        # store new point and set its connection
        self.connectionPoint = new
        self.connectionPoint.SetConnection(self)
        
        return
    
    def SetType(self, type):
        # swap type and spread
        result = self.connectionPoint.CanTypeBeSpread(type, extern=True)
        if result:
            print ("Type can be spread")
            self.connectionPoint.SpreadType(type, extern=True)
            self.type = type
            return True
        
        print ("Cannot change type of point")
        
        return False
    
    def GetType(self):
        # return electrical connection type
        return self.type

    # extra function to initialize a move
    def MoveInit(self):
        # notify point
        self.connectionPoint.OnPointMoveInit()
        
        return
    
    # move the point
    def Move(self, dX, dY):
        # call element function
        super().Move(dX, dY)
        
        # notify point that is has been moved
        self.connectionPoint.OnPointMove(dX, dY)
        
        return
    
    # extra function to exit a move
    def MoveExit(self):
        # notify point
        self.connectionPoint.OnPointMoveExit()
        
        return