from graphical.segmentclass import *
from graphical.graphicalconfig import *

from network.payloads.gridelementconfigs.pointconfig import *

class Point:
    def __init__(self, editorPage, posX, posY, type):
        # store data
        self.editorPage = editorPage
        self.posX = posX
        self.posY = posY
        self.type = type
        self.connection = None
        self.valid = True
        self.id = -1
        self.nodeId = -1;
        
        # variables for net extension
        self.oldX = posX
        self.oldY = posY
        self.startDirection = 'none'
        self.intermediatePoint = None
        self.startingPoint = None
        
        # list of connected segments
        self.segmentList = []
        
        # add this point to the editor page
        self.editorPage.AppendPoint(self)
        
        # graphics of this point
        self.canvasCircle = None
        self.canvasDot = None
        
        # visited variables for type determination
        self.visited = False
        
        return
    
    # this function creates a dictionary for storing point data
    def GenerateSaveToFileData(self, gridFile):
        # create a new dictianry and fill
        config = {}
        
        config["positionX"] = self.posX
        config["positionY"] = self.posY
        config["electricalType"] = self.type
        config["id"] = self.id
        config["nodeId"] = self.nodeId
        config["type"] = self.type
        
        return config
    
    # this function setups the point from a file config
    def GenerateFromFileData(self, config, gridFile):
        # set position, type and id
        self.posX = config["positionX"]
        self.posY = config["positionY"]
        self.type = config["electricalType"]
        self.id = config["id"]
        self.nodeId = config["nodeId"]
        self.type = config["type"]
        
        # update graphics
        self.UpdateGraphics()
        
        return
    
    @staticmethod
    def CreatePointGridConfiguration(config):
        # get position, type and id
        posX = config["positionX"]
        posY = config["positionY"]
        id = config["id"]
        nodeId = config["nodeId"]
        
        return PointConfig(id=id, nodeId=nodeId, rsvd=0, posX=posX, posY=posY)

    # call this functions when the point is to be deleted
    def DeletePoint(self):
        # check if point can be deleted
        if len(self.segmentList) != 0:
            print ("Point cannot be deleted!")
            return
        
        print (self)
        
        # remove graphical elements from canvas
        self.DrawAsNone()
        
        # remove point from editor page
        self.editorPage.RemovePoint(self)
        
        self.valid = False
        
        return
    
    def ConnectSegment(self, segment):
        # store segment in list
        if segment in self.segmentList:
            print ("Segment already in list")
            return
        
        self.segmentList.append(segment)
        
        segment.ConnectPoint(self)
        
        self.UpdateGraphics()
        
        return
    
    def DisconnectSegment(self, segment):
        # remove segment from list
        if segment in self.segmentList:
            self.segmentList.remove(segment)
            segment.DisconnectPoint(self)
        
        self.UpdateGraphics()
        
        return
    
    def SegmentRemoved(self):
        # segment notifies point that it has been removed
        # check if point has no connected segments anymore
        if self.connection:
            return
        
        if len(self.segmentList) != 0:
            # there are segments connected, so the type might be changed here
            t = self.DetermineType()
            
            # spread the determined type
            self.SpreadType(t)
            return
        
        # point is cleared, remove from editor page
        self.DeletePoint()
        
        return
    
    def SetConnection(self, connection):
        # set connection and redraw
        self.connection = connection
        
        self.UpdateGraphics()
        
        return
    
    def ConnectionRemoved(self, keep=False):
        # element notifies point that it has been removed
        # clear connection
        self.connection = None
        
        # check if segment list is also cleared
        if len(self.segmentList) != 0:
            # there are segments connected, so the points is kept but the type needs to be determined
            t = self.DetermineType()
            
            # spread the determined type
            self.SpreadType(t)
            return
        
        if keep:
            # keep this point
            return
        
        # point is cleared, remove from editor page
        self.DeletePoint()
        
        return
    
    # check if a certain type can be spread
    def CanTypeBeSpread(self, type, extern=False):
        # return if already visited
        if self.visited:
            return True
        
        # check if connection can be changed
        if self.connection and extern == False:
            if self.type != type:
                return False
        
        # visit
        self.visited = True
        
        # iterate over all segments and spread type further
        result = True
        for s in self.segmentList:
            p = s.GetOtherPoint(self)
            if not p:
                continue
            result &= p.CanTypeBeSpread(type)
        
        self.visited = False
        return result
    
    # spread a specific type over the net
    def SpreadType(self, type, extern=False):
        # return if this point was already visited
        if self.visited:
            return
        
        # now this is visited
        self.visited = True
        
        # store new type
        if self.connection and extern == False:
            if self.type != type:
                print ("Overriding connection type!")        
        
        # iterate over all segments and spread type further
        for s in self.segmentList:
            p = s.GetOtherPoint(self)
            if not p:
                continue
            p.SpreadType(type)
        
        # restore visited variable
        self.type = type
        self.visited = False
        
        # update graphics
        self.UpdateGraphics()
        
        for s in self.segmentList:
            s.UpdateGraphics()
        
        return
    
    def DetermineType(self):
        # check if we already visited this point
        if self.visited:
            return 'none'
        
        # now this is visited
        self.visited = True
        
        # check own type
        type = 'none'
        if self.connection:
            type = self.connection.GetType()
        
        else:
            # iterate over all other segments to find specific type
            for s in self.segmentList:
                p = s.GetOtherPoint(self)
                if not p:
                    continue
                t = p.DetermineType()
                if t != 'none':
                    type = t
                    break
        
        # restore visited variable
        self.visited = False
        
        return type
    
    # builds up a list of connectd points
    def BuildConnectedPointsList(self, connectedPoints):
        # first check if this point is already in list
        if self in connectedPoints:
            # nothing to do here, already visited
            return connectedPoints
        
        connectedPoints.append(self)
        
        # iterate over all segments and find other points
        for s in self.segmentList:
            other = s.GetOtherPoint(self)
            connectedPoints = other.BuildConnectedPointsList(connectedPoints)
        
        return connectedPoints
    
    # updates the graphics of the point
    def UpdateGraphics(self):
        # point has three states, circle, dot or none
        if self.connection:
            if len(self.segmentList) == 0:
                # draw as circle
                self.DrawAsCircle()
            elif len(self.segmentList) == 1:
                # draw nothing
                self.DrawAsNone()
            else:
                # draw as dot
                self.DrawAsDot()
        else:
            if len(self.segmentList) == 1:
                # draw as circle
                self.DrawAsCircle()
            elif len(self.segmentList) == 2:
                # draw nothing
                self.DrawAsNone()
            else:
                # draw as dot
                self.DrawAsDot()
        
        return

    # clear point graphics
    def DrawAsNone(self):
        # remove any graphics from canvas if needed
        canvas = self.editorPage.GetCanvas()
        
        if self.canvasCircle:
            canvas.delete(self.canvasCircle)
            self.canvasCircle = None
        
        if self.canvasDot:
            canvas.delete(self.canvasDot)
            self.canvasDot = None
        
        return
    
    def DrawAsCircle(self):
        # get canvas to work with
        canvas = self.editorPage.GetCanvas()
        
        # remove dot if needed
        if self.canvasDot:
            canvas.delete(self.canvasDot)
            self.canvasDot = None
        
        # create new circle
        if self.canvasCircle:
            # adapt coords
            canvas.coords(self.canvasCircle, self.posX - 4, self.posY - 4, self.posX + 3, self.posY + 3)
            canvas.itemconfig(self.canvasCircle, outline=GetColorByType(self.type))
            return
        
        self.canvasCircle = canvas.create_oval(self.posX - 4, self.posY - 4, self.posX + 3, self.posY + 3, outline=GetColorByType(self.type), width = 2)
        
        return
    
    def DrawAsDot(self):
        # get canvas to work with
        canvas = self.editorPage.GetCanvas()
        
        # remove circle if needed
        if self.canvasCircle:
            canvas.delete(self.canvasCircle)
            self.canvasCircle = None
        
        # create new dot
        if self.canvasDot:
            # adapt coords
            canvas.coords(self.canvasDot, self.posX - 4, self.posY - 4, self.posX + 3, self.posY + 3)
            canvas.itemconfig(self.canvasDot, outline=GetColorByType(self.type), fill=GetColorByType(self.type))
            return
        
        self.canvasDot = canvas.create_oval(self.posX - 4, self.posY - 4, self.posX + 3, self.posY + 3, outline=GetColorByType(self.type), fill=GetColorByType(self.type))
        
        return
    
    # check if point is at specific location
    def IsOnPoint(self, posX, posY):
        if self.posX == posX and self.posY == posY:
            return True
        return False
    
    # Join two points
    def JoinPoints(self, other):
        # check if this point is still valid
        if not self.valid:
            return False
        
        # check if the position matches
        if other.posX != self.posX or other.posY != self.posY:
            # points cannot be joined
            return False
        
        # check if points have the same type or of type none
        if self.type == 'none':
            # spread type of other point into this one
            self.SpreadType(other.type)
        
        elif other.type == 'none':
            # spread own type to other point
            other.SpreadType(self.type)
            
        if self.type != other.type:
            # points of different types cannot be joined
            return False
        
        # check if there is already a connection between these two points
        intersection = set(self.segmentList).intersection(other.segmentList)
        connected = len(intersection) != 0
        
        if connected:
            # if both points are element connections, nothing to do here
            if self.connection != None and other.connection != None:
                return False
            else:
                # break the existing segment
                for e in intersection:
                    # remove segment from both points
                    self.DisconnectSegment(e)
                    other.DisconnectSegment(e)
                    
                    # delete segment
                    e.DeleteSegment()
                
                # call JoinPoints again as there should be no intersection anymore
                self.JoinPoints(other)
        else:
            # if both points are element connections, create new zero length segment
            if self.connection != None and other.connection != None:
                s = Segment(self.editorPage)
                
                # connect segment to both points
                self.ConnectSegment(s)
                other.ConnectSegment(s)
            
            else:
                # only one or no point is an element connection, determine which one to keep
                toKeep = self
                toRemove = other
                
                if other.connection != None:
                    # swap
                    other.connection.SwapConnectionPoint(self)
                
                # swap segments from point to be removed to other point
                for s in toRemove.segmentList.copy():
                    toRemove.DisconnectSegment(s)
                    toKeep.ConnectSegment(s)
                
                # remove point from editor page
                toRemove.DeletePoint()
        
        # remove duplicate segments
        self.RemoveDuplicateSegments()
        
        return True
    
    def JoinSegments(self):
        # check if this point is still valid
        if not self.valid:
            return False
        
        # check if two segments are connected which have the same orientation
        if len(self.segmentList) != 2:
            return False
        
        if self.segmentList[0].orientation != self.segmentList[1].orientation:
            return False
        
        # check if this point can be removed
        if self.connection != None:
            # element connections cannot be removed
            return False
        
        # we can join the two segments
        # get the two points to be directly connected now
        s0 = self.segmentList[0]
        s1 = self.segmentList[1]
        p1 = s1.GetOtherPoint(self)
        
        # clean up       
        p1.DisconnectSegment(s1)
        self.DisconnectSegment(s0)
        self.DisconnectSegment(s1)
        
        # connect segment 0 to new point
        p1.ConnectSegment(s0)
        
        # remove this point and segment 1 from editor page
        self.DeletePoint()
        s1.DeleteSegment()
        
        return
    
    # split the given segment and add this point
    def SplitSegment(self):
        # check if this point is still valid
        if not self.valid:
            return False
        
        # search for a segment to split
        toSplit = None
        for s in self.editorPage.GetSegmentList():
            if s.IsInSegment(self):
                toSplit = s
                break
        else:
            # nothing to do here
            print ("no segment to split for this point")
            return False
        
        # check if points have the same type or are of type none
        other = toSplit.GetPoint(0)
        if self.type == 'none':
            # spread type of other point into this one
            self.SpreadType(other.type)
        
        elif other.type == 'none':
            # spread own type to other point
            other.SpreadType(self.type)
            
        if self.type != other.type:
            # points of different types cannot be joined
            return
        
        # remove point 1 from given segment
        p1 = toSplit.GetPoint(1)
        if not p1:
            return False
        
        p1.DisconnectSegment(toSplit)
        
        # connect given segment to this point
        self.ConnectSegment(toSplit)
        
        # create new segment to fill gap
        s1 = Segment(self.editorPage)
        p1.ConnectSegment(s1)
        self.ConnectSegment(s1)
        
        # check if we have created a double segment connection (might happen during dragging or extending the net)
        self.RemoveDuplicateSegments()
        
        return True
    
    # remove duplicate segments
    def RemoveDuplicateSegments(self):
        pl = []
        for s in self.segmentList:
            # other end
            p = s.GetOtherPoint(self)
            
            # check if already in connected points
            if p in pl:
                # remove segment and connection
                self.DisconnectSegment(s)
                p.DisconnectSegment(s)
                p.JoinSegments()
                
                s.DeleteSegment()
            
            else:
                # add point to connected list
                pl.append(p)
        
        return
    
    def OnPointDragInit(self):
        # this is called by a callback function from canvas
        # start with storing the old coords
        self.oldX = self.posX
        self.oldY = self.posY
        
        # create two new segments and points
        # starting point is copy of this one
        self.startingPoint = Point(self.editorPage, self.posX, self.posY, self.type)
        if self.connection != None:
            # swap connection point at grid device
            self.connection.SwapConnectionPoint(self.startingPoint, keep=True)
            self.connection = None
        
        # swap own segments to newly created point
        for s in self.segmentList.copy():
            self.DisconnectSegment(s)
            self.startingPoint.ConnectSegment(s)
        
        # create an intermediate point
        self.intermediatePoint = Point(self.editorPage, self.posX, self.posY, self.type)
        
        # create two segments to connect the three points
        s1 = Segment(self.editorPage)
        s2 = Segment(self.editorPage)
        
        self.startingPoint.ConnectSegment(s1)
        self.intermediatePoint.ConnectSegment(s1)
        
        self.intermediatePoint.ConnectSegment(s2)
        self.ConnectSegment(s2)
        
        return
    
    def OnPointDrag(self, posX, posY):
        # drag point and adjust intermediate point accordingly
        if posX == self.oldX and posY == self.oldY:
            # reset starting direction
            self.startDirection = 'none'
        
        # adjust starting direction
        if self.startDirection == 'none':
            if abs(self.oldX - posX) != 0:
                # horizontal movement first
                self.startDirection = 'h'
            elif abs(self.oldY - posY) != 0:
                # vertical movement first
                self.startDirection = 'v'
        
        # set intermediate point position
        if self.startDirection == 'h':
            self.intermediatePoint.posX = posX
            self.intermediatePoint.posY = self.oldY
        elif self.startDirection == 'v':
            self.intermediatePoint.posX = self.oldX
            self.intermediatePoint.posY = posY
        
        # store new coords
        self.posX = posX
        self.posY = posY
        
        # update all segments connected to this point
        for s in self.segmentList:
            s.UpdateGraphics()
        
        for s in self.intermediatePoint.segmentList:
            s.UpdateGraphics()
        
        return
    
    def OnPointDragExit(self):
        # update all segments connected to this point
        for s in self.segmentList:
            s.Update()
        
        for s in self.intermediatePoint.segmentList:
            s.Update()
        
        # try to join this point to some other point
        pl = self.editorPage.GetPointList().copy()
        try:
            # remove this point from list
            pl.remove(self)
            pl.remove(self.intermediatePoint)
            pl.remove(self.startingPoint)
        except:
            pass
        
        for p in pl:
            if self.IsOnPoint(p.posX, p.posY):
                # points share same location, merge
                self.JoinPoints(p)
        
        # try to join intermediate point to new endpoint
        result = self.JoinPoints(self.intermediatePoint)
        if result:
            # intermediate point was on endpoint, try to join endpoint with starting point
            result = self.JoinPoints(self.startingPoint)
            
            if result:
                # all points were at same location, it is already cleaned up here
                print ("All points at same location")
            else:
                # try to connect the endpoint to something and remove starting point if possible
                self.SplitSegment()
                self.startingPoint.JoinSegments()
        else:
            # intermediate point is free, try to connect endpoint to something and remove starting point if possible
            self.SplitSegment()
            self.startingPoint.JoinSegments()
        
        self.intermediatePoint = None
        self.startingPoint = None
        self.startDirection = 'none'
        
        # update own graphics
        self.UpdateGraphics()
        
        return
    
    def OnSegmentMoveInit(self, segment):
        print ("OnSegmentMoveInit")
        # this initializes a move called by a segment drag
        # function depends on type of point
        if self.connection == None:
            # no connection, this point is either an endpoint, a corner or a junction
            if len(self.segmentList) <= 2:
                # endpoint or corner, nothing to do here, point can be moved easily
                return
        
        # this point is either a junction or an endpoint, in both cases create a new segment and point
        # create a new point which replaces this one at the moved segment
        p = Point(self.editorPage, self.posX, self.posY, self.type)
        s = Segment(self.editorPage)
        
        # remove this point from dragged segment and connect newly created point
        self.DisconnectSegment(segment)
        p.ConnectSegment(segment)
        
        # add newly created segment to new point and this point
        p.ConnectSegment(s)
        self.ConnectSegment(s)

        return
    
    def OnSegmentMove(self, segment, dX, dY):
        # move point, if and only if there are two or less segments connected and this is no device connection
        if self.connection == None:
            if len(self.segmentList) <= 2:
                # add delta X and Y
                self.posX += dX
                self.posY += dY
        
        # update connected segments
        for s in self.segmentList:
            s.Update()
        
        # update own graphics
        self.UpdateGraphics()
        
        return
    
    def OnSegmentMoveExit(self, segment):
        # iterate over all points on page and check if this point can be merged
        pl = self.editorPage.GetPointList().copy()
        try:
            # remove this point from list
            pl.remove(self)
        except:
            pass
        
        for p in pl:
            if self.IsOnPoint(p.posX, p.posY):
                # points share same location, merge
                self.JoinPoints(p)
        
        # try to remove obsolete points
        self.JoinSegments()

        # try to split a segment if stopped on it
        self.SplitSegment()
        
        # update connected segments
        for s in self.segmentList:
            s.UpdateGraphics()
        
        return
    
    def OnPointMoveInit(self):
        # this is only called by a block connection, create a segment move from this if there are any segments
        for e in self.segmentList:
            # call segment move on this segment
            e.OnSegmentMoveInit(self)
        
        return
    
    def OnPointMove(self, dX, dY):
        # actual point move
        self.posX += dX
        self.posY += dY
        
        for e in self.segmentList:
            # move segment
            e.OnSegmentMove(self, dX, dY)
        
        self.UpdateGraphics()
        
        return
    
    def OnPointMoveExit(self):
        # end point move
        if len(self.segmentList) != 0:
            for e in self.segmentList:
                # end
                e.OnSegmentMoveExit(self)