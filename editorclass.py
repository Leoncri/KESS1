import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

from PIL import Image, ImageTk

from graphical.editorpageclass import *
from graphical.pointclass import *
from graphical.segmentclass import *
from devices.fenswitchgeardeviceclass import *
from devices.converterdevice import *
from devices.sourcedevice import *
from devices.scibreakbreakerdeviceclass import *
from network.networkinterface import *
from file.filedata import *

from network.headers.header import DeviceType
from network.packets.fenswitchgearrespond import *
from auxillary.windowsizetracker import *
from scope.scopemanager import *

from servermanager import *

class EditorMain:
    def __init__(self):
        # first create the main window
        self.window = tk.Tk()
        self.window.title("PGS Grid Editor - New File")
        self.window.protocol("WM_DELETE_WINDOW", self.OnExit)
        
        # create icon
        self.icon = ImageTk.PhotoImage(file = "icon.png")
        #self.window.wm_iconphoto(False, self.icon)
        
        # create window size tracker
        self.windowSizeTracker = WindowSizeTracker(self.window, self.OnWindowResize)
        
        # create editor page
        self.editorPageFrame = tk.Frame(self.window)
        self.editorPageFrame.grid(row=0, column=0)
        self.editorPage = EditorPage(self.editorPageFrame)
        
        # create info label
        self.infoLabel = tk.Label(self.window, text="Not connected")
        self.infoLabel.grid(row=1, column=0)
        
        # network handler class
        self.networkInterface = NetworkInterface(self)
        
        # server handler
        self.serverManager = ServerManager(self, self.networkInterface)
        
        # scope handler
        self.scopeManager = ScopeManager(self.window)
        
        # file data class
        self.fileData = GridFile(self, self.editorPage, self.networkInterface, self.scopeManager)
        self.networkInterface.SetGridFile(self.fileData)

        # create fiel menu
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        
        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New", command=self.OnNew)
        self.fileMenu.add_command(label="Open...", command=self.OnOpen)
        self.fileMenu.add_command(label="Save", command=self.OnSave)
        self.fileMenu.add_command(label="Save as...", command=self.OnSaveAs)
        #self.fileMenu.add_command(label="Config", command=self.OnConfig)
        self.fileMenu.add_command(label="Exit", command=self.OnExit)
        
        # menu for adding new components
        self.addMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Add", menu=self.addMenu)
        self.addMenu.add_command(label="New FEN Switchgear", command=self.OnNewFENSwitchgear)
        self.addMenu.add_command(label="New Converter", command=self.OnNewConverter)
        self.addMenu.add_command(label="New Source", command=self.OnNewSource)
        self.addMenu.add_command(label="New SciBreak Breaker", command=self.OnNewSciBreakBreaker)
        
        # network menu
        self.networkMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Network", menu=self.networkMenu)
        self.networkMenu.add_command(label="Connect to Server", command=self.OnConnectToServer)
        self.networkMenu.add_command(label="Upload File to Server", command=self.OnUploadToServer, state="disabled")
        self.networkMenu.add_command(label="Download File from Server", command=self.OnDownloadFromServer, state="disabled")
        self.networkMenu.add_command(label="Disconnect from Server", command=self.OnDisconnectFromServer, state="disabled")
        
        # grid menu
        self.gridMenu =tk.Menu(self.menu)
        self.menu.add_cascade(label="Grid", menu=self.gridMenu)
        self.gridMenu.add_command(label="Start Grid", command=self.OnStartGrid, state="disabled")
        self.gridMenu.add_command(label="Stop Grid", command=self.OnStopGrid, state="disabled")
        
        # scope menu
        self.scopeMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Scope", menu=self.scopeMenu)
        self.scopeMenu.add_command(label="Connect to Scope", command=self.OnConnectToScope)
        self.scopeMenu.add_command(label="Disconnect from Scope", command=self.OnDisconnectFromScope)
        self.scopeMenu.add_command(label="Scope Config", command=self.OnScopeConfig)
        
        self.filename = ""
        self.recentUpload = False
        self.recentDownload = False
        
        # list of devices
        self.deviceList = []
        
        # just generate some basic stuff
        p1 = Point(self.editorPage, 100, 100, 'none')
        p2 = Point(self.editorPage, 300, 100, 'none')
        s1 = Segment(self.editorPage)
        
        p1.ConnectSegment(s1)
        p2.ConnectSegment(s1)
    
    # add a device
    def AppendDevice(self, device):
        if device not in self.deviceList:
            print ("Adding device with id " + str(len(self.deviceList)))
            device.deviceID = len(self.deviceList)
            self.deviceList.append(device)
        return
    
    # remove a device
    def RemoveDevice(self, device):
        try:
            self.deviceList.remove(device)
            # reset device IDs
            counter = 0
            for e in self.deviceList:
                e.deviceID = counter
                counter += 1
        except:
            pass
        
        return
    
    # set the connection status
    def ChangedNetworkStatus(self):
        # change menu according to status
        self.ChangeGridOptions()
        
        return
    
    def ChangedServerStatus(self):
        # change menu according to status
        self.ChangeGridOptions()
        
        return
    
    def GridNotUpToDate(self):
        # if the grid was recently uploaded, return true to notify server manager that this was intended
        if self.recentUpload:
            self.recentUpload = False
            return True
        
        if self.recentDownload:
            self.recentDownload = False
            return True
        
        return False
    
    # callback for a new incoming normal packet
    def NewPacket(self, packet):
        if packet.header.deviceType == DeviceType.SERVER:
            self.serverManager.NewPacket(packet)
        else:
            # forward packet to device with specific id
            id = packet.header.deviceId
            
            for e in self.deviceList:
                if e.deviceID == id:
                    e.HandleNewPacket(packet)
        
        return
    
    # callback for creating a new file
    def OnNew(self):
        # check if progress needs to be saved
        if self.editorPage.HasChanged():
            # ask for save
            result = tkinter.messagebox.askquestion(title="Save progress?", message="Do you want to save your progress?")
        
            if result == "yes":
                if self.filename != "":
                    self.OnSave()
                else:
                    self.OnSaveAs()
        
        # clear page
        self.editorPage.Clear()
        
        self.filename = ""
        
        self.window.title("PGS Grid Editor - New File")
        
        return
    
    # open a new file
    def OnOpen(self):
        # ask for filename
        filename = tkinter.filedialog.askopenfilename()
        
        if not filename:
            return
        
        # create a new file
        self.OnNew()
        
        self.filename = filename
        
        # read in filename
        result = self.fileData.OpenFromFile(filename)
        
        self.window.title("PGS Grid Editor - " + self.filename)
        
        return
    
    # save a file
    def OnSave(self):
        # filename?
        if self.filename == "":
            self.OnSaveAs()
        
        # save to file
        points = self.editorPage.GetPointList()
        segments = self.editorPage.GetSegmentList()
        elements = self.editorPage.GetElementList()
        
        self.fileData.SaveToFile(self.filename, points, segments, elements, "editor")
        
        self.window.title("PGS Grid Editor - " + self.filename)
        
        return
    
    # save to file
    def OnSaveAs(self):
        # ask for filename
        filename = tkinter.filedialog.asksaveasfilename()
        
        if not filename:
            return
        
        self.filename = filename
        
        self.OnSave()
        
        return
    
    def OnExit(self):
        # ask if element should be saved
        if self.editorPage.HasChanged():
            result = tkinter.messagebox.askquestion(title="Save progress?", message="Do you want to save your progress?")
        
            if result == "yes":
                if self.filename != "":
                    self.OnSave()
                else:
                    self.OnSaveAs()
        
        self.window.destroy()
        
        return
    
    def OnNewFENSwitchgear(self):
        # create a new fen switchgear
        switchgear = FENSwitchgearDevice(self, self.editorPage, self.networkInterface, self.scopeManager)
        
        switchgear.CreateNewFENSWitchgear(300, 300)
        
        return
    
    def OnNewConverter(self):
        # create a new converter
        converter = ConverterDevice(self, self.editorPage, self.networkInterface, self.scopeManager)
        
        converter.CreateNewConverter(300, 300)
        
        return
    
    def OnNewSciBreakBreaker(self):
        # create a new scibreak breaker
        breaker = SciBreakBreakerDevice(self, self.editorPage, self.networkInterface, self.scopeManager)
        
        breaker.CreateNewSciBreakBreaker(300, 300)
        
        return
    
    def OnNewSource(self):
        # create a new source
        source = GridSource(self, self.editorPage, self.networkInterface, self.scopeManager)
        
        source.CreateNewSource(300, 300)
        
        return
    
    def OnConnectToServer(self):
        self.networkInterface.ConnectToServer(self.window)
        return
    
    def OnUploadToServer(self):
        # upload to server
        points = self.editorPage.GetPointList()
        segments = self.editorPage.GetSegmentList()
        elements = self.editorPage.GetElementList()
        
        result = self.fileData.UploadToServer(self.filename + "_network", points, segments, elements)
        if result:
            self.recentUpload = True
        
        return
    
    def OnDownloadFromServer(self):
        # create a new file
        self.OnNew()
        
        # download from server
        result = self.fileData.DownloadFromServer("network_download.json")
        if result:
            print ("Successfully downloaded data")
            self.recentDownload = True
        
        return
    
    def OnDisconnectFromServer(self):
        self.networkInterface.Disconnect()
        self.ChangeGridOptions()
        self.editorPage.ChangeToEditorMode()
        self.serverManager.Reset()
        return
    
    def OnStartGrid(self):
        # try to start the grid
        result = self.serverManager.StartGrid()
        if not result:
            return
        
        # change menu
        self.ChangeGridOptions()
        
        return
    
    def OnStopGrid(self):
        # try to stop the grid
        result = self.serverManager.StopGrid()
        if not result:
            return
        
        # change menu
        self.ChangeGridOptions()
        
        return
    
    def OnWindowResize(self, width, height):
        # notify editor page to change
        self.editorPage.CanvasResize(width - 4, height - 25)
        
        return
    
    def ChangeGridOptions(self):
        # disable all menu entries
        allowConnect = "disabled"
        allowUpload = "disabled"
        allowDownload = "disabled"
        allowDisconnect = "disabled"
        allowStart = "disabled"
        allowStop = "disabled"
        
        # connected?
        if not self.networkInterface.IsConnected():
            # disable all menu entries except connect
            allowConnect = "normal"
            
            self.infoLabel["text"] = "Not connected to server"
            
            # change to editor mode
            self.editorPage.ChangeToViewMode()
            
        else:
            # start and stop
            upToDate, loaded, started = self.serverManager.GetGridStatus()
            
            if upToDate:
                # grid is already downloaded and up to date
                # change to view mode
                self.editorPage.ChangeToViewMode()
                
                # allow start/stop and upload
                if started:
                    # allow stop
                    allowStop = "normal"
                else:
                    # allow start and upload
                    allowStart = "normal"
                    allowUpload = "normal"
            
            else:
                # change to editor mode
                self.editorPage.ChangeToEditorMode()
                
                # allow download and upload
                if loaded:
                    if started:
                        # only allow stop
                        allowStop = "normal"
                    else:
                        # allow upload and download
                        allowUpload = "normal"
                        allowDownload = "normal"
                else:
                    # only allow upload
                    allowUpload = "normal"
            
            self.infoLabel["text"] = "Connected to: " + self.networkInterface.ip + " | " + str(self.networkInterface.port)
            allowDisconnect = "normal"
        
        # set the states
        self.networkMenu.entryconfig('Connect to Server', state=allowConnect)
        self.networkMenu.entryconfig("Upload File to Server", state=allowUpload)
        self.networkMenu.entryconfig("Download File from Server", state=allowDownload)
        self.networkMenu.entryconfig("Disconnect from Server", state=allowDisconnect)
        self.gridMenu.entryconfig("Start Grid", state=allowStart)
        self.gridMenu.entryconfig("Stop Grid", state=allowStop)
        
        return
    
    def OnConnectToScope(self):
        self.scopeManager.ConnectToScope()
        return
    
    def OnDisconnectFromScope(self):
        self.scopeManager.DisconnectFromScope()
        return
    
    def OnScopeConfig(self):
        self.scopeManager.OpenConfigWindow()
        return
    
    def Mainloop(self):
        self.window.mainloop()