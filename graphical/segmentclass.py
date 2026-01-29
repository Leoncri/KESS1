from graphical.pointclass import *
from graphical.graphicalconfig import *

from network.payloads.gridelementconfigs.segmentconfig import *

class Segment:
    def __init__(self, editorPage):
        # the two points for this segment
        self.pointList = []
        
        # editor page where the segment is
        self.editorPage = editorPage
        
        # orientation of this segment
        self.orientation = 'none'
        
        # append segment to editor page
        self.editorPage.AppendSegment(self)
        
        # graphics
        self.canvasLine = None
    
    # this function creates a dictionary for storing segment data
    def GenerateSaveToFileData(self, gridFile):
        # create a new dictianry and fill
        config = {}
        
        config["point1Id"] = self.pointList[0].id
        config["point2Id"] = self.pointList[1].id
        
        return config
    
    # this function setups the segment from a file config
    def GenerateFromFileData(self, config, gridFile):
        # get points from id and connect
        gridFile.GetPointFromId(config["point1Id"]).ConnectSegment(self)
        gridFile.GetPointFromId(config["point2Id"]).ConnectSegment(self)
        
        # update graphics
        self.Update()
        
        return
    
    @staticmethod
    def CreateSegmentGridConfiguration(config):
        # get point IDs
        point1Id = config["point1Id"]
        point2Id = config["point2Id"]
        
        return SegmentConfig(id=0, point1Id=point1Id, point2Id=point2Id)
    
    def DeleteSegment(self):
        # delete this segment if there are no more points connected
        if len(self.pointList) != 0:
            print ("Trying to remove segment with points connected!")
        
        self.editorPage.RemoveSegment(self)
        
        # remove graphics
        self.RemoveGraphics()
        
        return
    
    def ConnectPoint(self, p):
        # check if point can be connected
        if len(self.pointList) < 2 and p not in self.pointList:
            self.pointList.append(p)
        else:
            print ("Warning: Cannot attach segment to point")
        
        self.DetermineOrientation()
        
        # update graphics
        self.UpdateGraphics()
        
        return
    
    def DisconnectPoint(self, p):
        # remove point from list
        try:
            self.pointList.remove(p)
            
            # break orientation
            self.orientation = 'none'
        except:
            print ("Cannot remove point from segment")
        
        # update graphics
        self.UpdateGraphics()
        
        return
    
    def DetermineOrientation(self):
        if len(self.pointList) == 2:
            # set orientation
            if self.pointList[0].posX == self.pointList[1].posX:
                # same horizontal position gives vertical segment
                self.orientation = 'v'
            elif self.pointList[0].posY == self.pointList[1].posY:
                # same vertical position gives horizontal segment
                self.orientation = 'h'
            else:
                # error, something is wrong
                self.orientation = 'none'
                print ("Cannot determine segment orientation!")
        
        return
    
    def IsInSegment(self, p):
        # check if point falls in segment
        if self.orientation == 'h':
            if p.posY != self.pointList[0].posY:
                return False
            
            minX = min(self.pointList[0].posX, self.pointList[1].posX)
            maxX = max(self.pointList[0].posX, self.pointList[1].posX)
            
            if minX < p.posX and maxX > p.posX:
                return True
            return False
        
        elif self.orientation == 'v':
            if p.posX != self.pointList[0].posX:
                return False
            
            minY = min(self.pointList[0].posY, self.pointList[1].posY)
            maxY = max(self.pointList[0].posY, self.pointList[1].posY)
            
            if minY < p.posY and maxY > p.posY:
                return True
            return False
        
        return False
    
    def IsOnSegment(self, posX, posY):
        # check if position is on segment
        # check if point falls in segment
        if self.orientation == 'h':
            if posY != self.pointList[0].posY:
                return False
            
            minX = min(self.pointList[0].posX, self.pointList[1].posX)
            maxX = max(self.pointList[0].posX, self.pointList[1].posX)
            
            if minX <= posX and maxX >= posX:
                return True
            return False
        
        elif self.orientation == 'v':
            if posX != self.pointList[0].posX:
                return False
            
            minY = min(self.pointList[0].posY, self.pointList[1].posY)
            maxY = max(self.pointList[0].posY, self.pointList[1].posY)
            
            if minY <= posY and maxY >= posY:
                return True
            return False
        
        return False
    
    def IsCoveredBy(self, startX, startY, endX, endY):
        # return true if segment is within area
        minY = min(self.pointList[0].posY, self.pointList[1].posY)
        maxY = max(self.pointList[0].posY, self.pointList[1].posY)
        minX = min(self.pointList[0].posX, self.pointList[1].posX)
        maxX = max(self.pointList[0].posX, self.pointList[1].posX)
        
        # start is always top left
        if minX < startX:
            return False
        
        if maxX > endX:
            return False
        
        if minY < startY:
            return False
        
        if maxY > endY:
            return False
        
        return True
    
    # get the point connected to the other side
    def GetOtherPoint(self, p):
        # check if we already have to points
        if len(self.pointList) != 2:
            print ("Warning: Segments returns None as other point")
            return None
        
        pl = self.pointList.copy()
        
        if p in pl:
            pl.remove(p)
            return pl[0]
        
        print ("Warning: Segments returns None as other point")
        return None
    
    # get point with index from point list
    def GetPoint(self, index):
        try:
            return self.pointList[index]
        except:
            pass
        
        return None
    
    # update this segment
    def Update(self):
        # determine new orientation
        self.DetermineOrientation()
        
        # update graphics
        self.UpdateGraphics()
        
        return
    
    def UpdateGraphics(self):
        # create a line if needed and update the endpoints
        if len(self.pointList) != 2:
            # nothing to do here
            return
        
        canvas = self.editorPage.GetCanvas()
        
        xStart = self.pointList[0].posX
        yStart = self.pointList[0].posY
        xEnd = self.pointList[1].posX
        yEnd = self.pointList[1].posY
        
        # get type
        type = self.pointList[0].type
        
        if not self.canvasLine:
            # create a new line
            self.canvasLine = canvas.create_line(xStart, yStart, xEnd, yEnd, fill=GetColorByType(type), width=2)
        else:
            # redraw the line
            canvas.coords(self.canvasLine, xStart, yStart, xEnd, yEnd)
            canvas.itemconfig(self.canvasLine, fill=GetColorByType(type))
            
        return
    
    def Select(self, onOff):
        # check if there is a line to change
        if not self.canvasLine:
            return
        
        canvas = self.editorPage.GetCanvas()
        
        if onOff:
            # change the witdh of the line to 4
            canvas.itemconfig(self.canvasLine, width=4)
        else:
            # change the width back to 2
            canvas.itemconfig(self.canvasLine, width=2)
        
        return
    
    def RemoveGraphics(self):
        # remove the graphical line
        if self.canvasLine:
            canvas = self.editorPage.GetCanvas()
            canvas.delete(self.canvasLine)
        
        self.canvasLine = None
        
        return
    
    def OnRemove(self):
        # disconnect segment and notify points, this is for deleting a segment by user
        for p in self.pointList.copy():
            print ("Disconnecting segment from point")
            p.DisconnectSegment(self)
            p.SegmentRemoved()
        
        # remove this segment completely
        self.DeleteSegment()
        
        return
    
    # init a segment drag
    def OnSegmentDragInit(self):
        # initialize the drag by initializing the points
        for p in self.pointList:
            p.OnSegmentMoveInit(self)
        
        return
    
    # drag the segment
    def OnSegmentDrag(self, dX, dY):
        # check orientation
        if self.orientation == 'h':
            # only allow vertical movement
            dX = 0
        elif self.orientation == 'v':
            # only allow horizontal movement
            dY = 0
        else:
            dX = 0
            dY = 0
        
        # call handler for points
        for p in self.pointList:
            p.OnSegmentMove(self, dX, dY)
        
        return
    
    # end of drag
    def OnSegmentDragExit(self):
        # call handler for points
        for p in self.pointList:
            p.OnSegmentMoveExit(self)
        
        return
    
    # init move by point
    def OnSegmentMoveInit(self, point):
        # initializes a segment move for the other point
        p = self.GetOtherPoint(point)
        
        p.OnSegmentMoveInit(self)
        
        return
    
    # move by point
    def OnSegmentMove(self, point, dX, dY):
        # moves the other point
        p = self.GetOtherPoint(point)
        
        # move segment depending on orientation
        if self.orientation == 'h':
            # only move in y axis
            p.OnSegmentMove(self, 0, dY)
        elif self.orientation == 'v':
            # only move in x axis
            p.OnSegmentMove(self, dX, 0)
        
        return
    
    # exit move by point
    def OnSegmentMoveExit(self, point):
        # exit function for moving other point
        p = self.GetOtherPoint(point)
        
        p.OnSegmentMoveExit(self)
        
        return