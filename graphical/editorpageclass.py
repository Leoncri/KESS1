from graphical.pointclass import *
from graphical.segmentclass import *

from tkinter import *

class EditorPage:
    def __init__(self, masterWindow):
        # master window
        self.masterWindow = masterWindow
        
        # lists for storing points, segments and elements
        self.pointList = []
        self.segmentList = []
        self.elementList = []
        
        # lists of selected points, segments and elements
        self.selectedPoints = []
        self.selectedSegments = []
        self.selectedElements = []
        self.draggedPoint = None
        self.draggedSegment = None
        self.draggedElement = None
        self.selectionMode = 'none'
        self.selectionRectangle = None
        self.startPosX = 0
        self.startPosY = 0
        self.lastPosX = 0
        self.lastPosY = 0
        
        self.mode = "editor"
        self.hasChanged = True
        
        # graphical stuff
        self.canvas = Canvas(masterWindow, width=600, height=480)
        self.canvas.pack()
        self.canvas.focus_set()
        
        # bind mouse and keyboard functions
        self.canvas.bind("<ButtonPress-1>", self.OnLeftMouseClick)
        self.canvas.bind("<Double-Button-1>", self.OnDoubleLeftMouseClick)
        self.canvas.bind("<B1-Motion>", self.OnLeftMouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.OnLeftMouseRelease)
        self.canvas.bind("<Delete>", self.OnDeleteHandler)
        self.canvas.bind("<Control-r>", self.OnRotateElementsCW)
        self.canvas.bind("<Control-Shift-R>", self.OnRotateElementsCCW)
        
    
    def Clear(self):
        # clears the entire page
        for e in self.elementList.copy():
            e.OnDelete()
        
        for s in self.segmentList.copy():
            s.OnRemove()
        
        self.elementList.clear()
        self.segmentList.clear()
        self.pointList.clear()
        
        self.hasChanged = False
        
        self.mode = "editor"
        
        return
    
    def CanvasResize(self, width, height):
        self.canvas.config(width=width, height=height)
        return
    
    def ChangeToViewMode(self):
        self.mode = "viewer"
        return
    
    def ChangeToEditorMode(self):
        self.mode = "editor"
        return
    
    def HasChanged(self):
        return self.hasChanged
    
    def AppendPoint(self, p):
        # append given point to list
        if p not in self.pointList:
            self.pointList.append(p)
        
        return
    
    def RemovePoint(self, p):
        # remove point from list
        try:
            self.pointList.remove(p)
        except:
            pass
        
        return
    
    def GetPointList(self):
        # return the list of points
        return self.pointList
    
    def AppendSegment(self, s):
        # append given segment to list
        if s not in self.segmentList:
            self.segmentList.append(s)
        
        return
    
    def RemoveSegment(self, s):
        # remove given segment from list
        try:
            self.segmentList.remove(s)
        except:
            pass
        
        return
    
    def GetSegmentList(self):
        # return the list of segments
        return self.segmentList
    
    def AppendElement(self, element):
        # append given element to list
        if element not in self.elementList:
            self.elementList.append(element)
        
        return
    
    def RemoveElement(self, element):
        # remove element from list
        try:
            self.elementList.remove(element)
        except:
            pass
        
        return
    
    def GetElementList(self):
        # return the list of elements
        return self.elementList
    
    def GeneratePointIDs(self):
        # set the point id for every point
        counter = 0
        
        for p in self.pointList:
            p.id = counter
            counter += 1
        
        return
    
    # return the canvas to draw to
    def GetCanvas(self):
        return self.canvas
    
    def OnLeftMouseClick(self, event):
        # not used in viewer mode
        if self.mode =="viewer":
            return
        
        # adjust position of click
        posX = 10 * round(event.x / 10)
        posY = 10 * round(event.y / 10)
        self.startPosX = posX
        self.startPosY = posY
        self.lastPosX = posX
        self.lastPosY = posY
        
        # unselect all previously selected items        
        for s in self.selectedSegments:
            s.Select(False)
        
        for e in self.selectedElements:
            e.Select(False)
        
        # clear the lists
        self.selectedPoints.clear()
        self.selectedSegments.clear()
        self.selectedElements.clear()
        
        # select new points, segments and elements
        for p in self.pointList:
            if p.IsOnPoint(posX, posY):
                self.selectedPoints.append(p)
        
        for s in self.segmentList:
            if s.IsOnSegment(posX, posY):
                self.selectedSegments.append(s)
                s.Select(True)
        
        for e in self.elementList:
            if e.IsOnElement(posX, posY):
                self.selectedElements.append(e)
                e.Select(True)
        
        # check if there is something selected
        if len(self.selectedPoints) == 0 and len(self.selectedSegments) == 0 and len(self.selectedElements) == 0:
            # this would be area mode, done for now
            self.selectionMode = 'area'
            
            return
        
        if len(self.selectedPoints) != 0:
            # drag a point goes first
            print ("Point selected")
            self.selectionMode = 'point'
            self.draggedPoint = self.selectedPoints[0]
            self.draggedPoint.OnPointDragInit()
        
        elif len(self.selectedSegments) != 0:
            # drag a segment is next
            self.selectionMode = 'segment'
            self.draggedSegment = self.selectedSegments[0]
            self.draggedSegment.OnSegmentDragInit()
        
        elif len(self.selectedElements) != 0:
            # drag an element is last
            self.selectionMode = 'element'
            self.draggedElement = self.selectedElements[0]
            self.draggedElement.OnElementDragInit()
        
        return
    
    def OnLeftMouseDrag(self, event):
        # not used in viewer mode
        if self.mode == "viewer":
            return
        
        # adjust position of click
        posX = 10 * round(event.x / 10)
        posY = 10 * round(event.y / 10)
        
        # get dX and dY
        dX = posX - self.lastPosX
        dY = posY - self.lastPosY
        self.lastPosX = posX
        self.lastPosY = posY
        
        # call handler of selected item
        if self.selectionMode == 'area':
            # draw selection rectangle
            self.DrawSelectionRectangle(self.startPosX, self.startPosY, posX, posY)
            self.SelectUnderRectangle(self.startPosX, self.startPosY, posX, posY)
        
        elif self.selectionMode == 'point':
            # call drag on selected point
            self.draggedPoint.OnPointDrag(posX, posY)
        
        elif self.selectionMode == 'segment':
            # call drag on selected segment
            self.draggedSegment.OnSegmentDrag(dX, dY)
        
        elif self.selectionMode == 'element':
            # call drag on selected element
            self.draggedElement.OnElementDrag(dX, dY)
        
        return
    
    def OnLeftMouseRelease(self, event):
        # not used in viewer mode
        if self.mode == "viewer":
            return
        
        # adjust position of click
        posX = 10 * round(event.x / 10)
        posY = 10 * round(event.y / 10)
        
        # call handler of selected item
        if self.selectionMode == 'area':
            # clear selection rectangle and select everything under it
            self.ClearSelectionRectangle()
            self.SelectUnderRectangle(self.startPosX, self.startPosY, posX, posY)
        
        elif self.selectionMode == 'point':
            # call exit on dragged point
            self.draggedPoint.OnPointDragExit()
        
        elif self.selectionMode == 'segment':
            # call exit on dragged segment
            self.draggedSegment.OnSegmentDragExit()
        
        elif self.selectionMode == 'element':
            # call exit on dragged element
            self.draggedElement.OnElementDragExit()
        
        # clear used variables
        self.draggedPoint = None
        self.draggedSegment = None
        self.draggedElement = None
        self.selectionMode = 'none'
        
        return
    
    def OnDeleteHandler(self, event):
        # not used in viewer mode
        if self.mode == "viewer":
            return
        
        # delete all selected segments and elements, points will clear themself
        for s in self.selectedSegments:
            s.OnRemove()
        
        for e in self.selectedElements:
            e.OnDelete()
        
        # clear selected item lists
        self.selectedPoints = []
        self.selectedSegments = []
        self.selectedElements = []
        
        return
    
    def OnDoubleLeftMouseClick(self, event):
        # get x and y coords
        posX = event.x
        posY = event.y
        
        # open config for element
        for e in self.elementList:
            if e.IsOnElement(posX, posY):
                if self.mode == "viewer":
                    e.ShowControlConfigWindow("viewer")
                else:
                    e.ShowControlConfigWindow(self.mode)
                    #e.ShowControlConfigWindow("viewer")
        
        return
    
    def OnRotateElementsCW(self, event):
        # rotate all selected elements
        for e in self.selectedElements:
            e.OnRotateCW()
        
        return
    
    def OnRotateElementsCCW(self, event):
        # rotate all selected elements
        for e in self.selectedElements:
            e.OnRotateCCW()
        
        return
    
    def DrawSelectionRectangle(self, startX, startY, endX, endY):
        # check if the rectangle is already drawn
        if not self.selectionRectangle:
            self.selectionRectangle = self.canvas.create_rectangle(startX, startY, endX, endY, outline='black')
            return
        
        # adjust position
        self.canvas.coords(self.selectionRectangle, startX, startY, endX, endY)
        
        return
    
    def ClearSelectionRectangle(self):
        # delete the selection rectangle
        if self.selectionRectangle:
            self.canvas.delete(self.selectionRectangle)
        
        self.selectionRectangle = None
        
        return
    
    def SelectUnderRectangle(self, startX, startY, endX, endY):
        # sort start and end
        if startX > endX:
            startX, endX = endX, startX
        
        if startY > endY:
            startY, endY = endY, startY
        
        # select everything that falls fully inside the rectangle
        for s in self.segmentList:
            if s.IsCoveredBy(startX, startY, endX, endY):
                if s not in self.selectedSegments:
                    self.selectedSegments.append(s)
                    s.Select(True)
                    
            else:
                if s in self.selectedSegments:
                    self.selectedSegments.remove(s)
                    s.Select(False)
        
        newElements = []
        for e in self.elementList:
            if e.IsCoveredBy(startX, startY, endX, endY):
                if e not in self.selectedElements:
                    self.selectedElements.append(e)
                    e.Select(True)
            
            else:
                if e in self.selectedElements:
                    self.selectedElements.remove(e)
                    e.Select(False)
        
        return