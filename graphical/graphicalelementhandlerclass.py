from graphical.canvaslineclass import *
from graphical.canvasrectangleclass import *
from graphical.canvastextclass import *
from graphical.canvassmallswitch import *
from graphical.connectionpointclass import *
from graphical.pointclass import *

class GraphicalElementHandler:
    def __init__(self, device, editorPage, posX, posY, rotation):
        # store variables
        self.device = device
        self.editorPage = editorPage
        self.posX = posX
        self.posY = posY
        self.rotation = rotation
        
        # lists for elements
        self.graphicalElementsList = []
        self.graphicalElementsDict = {}
        
        # list for connections
        self.connectionList = []
        
        # create bounding box
        self.bBoxStartX = -20
        self.bBoxStartY = -20
        self.bBoxEndX = 20
        self.bBoxEndY = 20
        
        # append self to editor page
        self.editorPage.AppendElement(self)
    
    # generate the data to be stored in a file
    def GenerateSaveToFileData(self, gridFile):
        # forward to actual device
        return self.device.GenerateSaveToFileData(gridFile)
    
    # function to determine if position is in element
    def IsOnElement(self, posX, posY):
        # adjust position according to own position
        posX -= self.posX
        posY -= self.posY
        
        # sort bounding box
        maxX = max(self.bBoxStartX, self.bBoxEndX)
        minX = min(self.bBoxStartX, self.bBoxEndX)
        maxY = max(self.bBoxStartY, self.bBoxEndY)
        minY = min(self.bBoxStartY, self.bBoxEndY)
        
        if posX <= maxX and posX >= minX:
            if posY <= maxY and posY >= minY:
                return True
        
        return False
    
    def IsCoveredBy(self, startX, startY, endX, endY):
        # return true if element is within area
        # adjust position according to own position
        startX -= self.posX
        startY -= self.posY
        endX -= self.posX
        endY -= self.posY
        
        # sort bounding box
        maxX = max(self.bBoxStartX, self.bBoxEndX)
        minX = min(self.bBoxStartX, self.bBoxEndX)
        maxY = max(self.bBoxStartY, self.bBoxEndY)
        minY = min(self.bBoxStartY, self.bBoxEndY)
        
        if minX < startX:
            return False
        
        if maxX > endX:
            return False
        
        if minY < startY:
            return False
        
        if maxY > endY:
            return False
        
        return True
    
    # function to delete this element
    def OnDelete(self):
        # remove all graphical elements
        for e in self.graphicalElementsList:
            e.Delete()
        
        # delete all connections
        for e in self.connectionList:
            e.Delete()
        
        # clear lists
        self.graphicalElementsList.clear()
        self.graphicalElementsDict.clear()
        self.connectionList.clear()
        
        # notify device about delete
        self.device.Delete()
        
        # remove element from editor page
        self.editorPage.RemoveElement(self)
        
        return
    
    # select this element
    def Select(self, onOff):
        for e in self.graphicalElementsList:
            e.Select(onOff)
        return
    
    # function to initialize an element drag
    def OnElementDragInit(self):
        # iterate over every connection and initialize the drag
        for e in self.connectionList:
            e.MoveInit()
        
        return
    
    # function to drag an element
    def OnElementDrag(self, dX, dY):
        # call every graphical element and move it
        for e in self.graphicalElementsList:
            e.Move(dX, dY)
        
        # drag every connection point
        for e in self.connectionList:
            e.Move(dX, dY)
        
        # save own coords
        self.posX += dX
        self.posY += dY
        
        return
    
    # function for exiting an element drag
    def OnElementDragExit(self):
        # call every function and exit
        for e in self.connectionList:
            e.MoveExit()
        
        return
    
    # function to rotate the element
    def OnRotateCW(self):
        # rotate every element clockwise
        for e in self.graphicalElementsList:
            e.RotateCW()
        
        for e in self.connectionList:
            e.RotateCW()
        
        # rotate self
        self.rotation += 90
        if self.rotation >= 360:
            self.rotation = 0
        
        return
    
    def OnRotateCCW(self):
        # rotate every element counter-clockwise
        for e in self.graphicalElementsList:
            e.RotateCCW()
        
        for e in self.connectionList:
            e.RotateCCW()
        
        # rotate self
        self.rotation -= 90
        if self.rotation < 0:
            self.rotation += 360
        
        return
    
    # function to swap the points from a connection
    def SwapConnectionPoint(self, old, new):
        # iterate over every connection and swap if needed
        for e in self.connectionList:
            if e.connectionPoint == old:
                e.connectionPoint = new
        
        return
    
    # function to load in graphical elements
    def LoadGraphicalElements(self, graphicalData):
        # iterate over all elements
        for e in graphicalData:
            element = graphicalData[e]
            
            if e == "BOUNDING_BOX":
                # set bounding box
                self._SetBoundingBox(element)
            else:
                # append according to type
                type = element["type"]
                if type == "line":
                    self._AppendLineElement(e, element)
                elif type == "rectangle":
                    self._AppendRectangleElement(e, element)
                elif type == "text":
                    self._AppendTextElement(e, element)
                elif type == "schematicSwitch":
                    self._AppendSchematicSwitch(e, element)
            
        return
    
    # function to append a connection element
    def LoadConnections(self, gridFile, baseConnectionConfig, deviceConnectionConfig):
        # iterate over all connections
        for c in baseConnectionConfig:
            baseConnection = baseConnectionConfig[c]
            deviceConnection = deviceConnectionConfig[c]
            
            # check if this connection need a point
            try:
                pointID = deviceConnection["pointID"]
                # if pointId is negative, create a new point, otherwise get the point from the editor page
                if pointID < 0:
                    px = baseConnection["positionX"]
                    py = baseConnection["positionY"]
                    type = baseConnection["electricalType"]
                    point = Point(self.editorPage, self.posX + px, self.posY + py, type)
                else:
                    point = gridFile.GetPointFromId(pointID)
            
            except Exception as e:
                print (e)
                print ("Broken file, cannot determine a point for a connection.")
                return
        
            # create a new connection and add it to the list
            c = ConnectionPoint(self.editorPage.GetCanvas(), self.posX, self.posY, point, self.rotation)
            self.connectionList.append(c)
            point.SetConnection(c)
        
        return
    
    def ShowControlConfigWindow(self, mode):
        # call edit window for device
        self.device.ShowControlConfigWindow(mode)
    
    # function to append a line
    def _AppendLineElement(self, key, config):
        # create a new line
        line = CanvasLine(self.editorPage.GetCanvas(), self.posX, self.posY, config, self.rotation)
        
        self.graphicalElementsList.append(line)
        self.graphicalElementsDict[key] = line
        
        return
    
    # function to append a rectangle
    def _AppendRectangleElement(self, key, config):
        # create a new rectangle
        rect = CanvasRectangle(self.editorPage.GetCanvas(), self.posX, self.posY, config, self.rotation)
        
        self.graphicalElementsList.append(rect)
        self.graphicalElementsDict[key] = rect
        
        return
    
    def _AppendTextElement(self, key, config):
        # create a new text
        text = CanvasText(self.editorPage.GetCanvas(), self.posX, self.posY, config, self.rotation)
        
        self.graphicalElementsList.append(text)
        self.graphicalElementsDict[key] = text
        
        return
    
    def _AppendSchematicSwitch(self, key, config):
        # create a new schematic switch
        switch = CanvasSmallSwitch(self.editorPage.GetCanvas(), self.posX, self.posY, config, self.rotation, self.editorPage.masterWindow)
        
        self.graphicalElementsList.append(switch)
        self.graphicalElementsDict[key] = switch
        
        return