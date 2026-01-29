import tkinter as tk
import socket
import threading
import time
import struct
from generic.genericconfigwindowclass import *

class ScopeManager:
    """ this class manages the connection for a live view scope """
    def __init__(self, master):
        # store variables
        self.master = master
        
        # data sources
        self.channels = [None] * 8
        self.channelNames = [""] * 8
        self.channelScales = [1] * 8
        self.channelOffsets = [0] * 8
        
        
        # subwindow
        self.cWindow = None
        self.eWindow = None
        self.listbox = None
        
        # scope connection
        self.scopeIP = ""
        self.scopePort = 0
        self.scopeConnected = False
        self.scopeSocket = None
        self.scopeRunThread = False
        self.scopeThread = None
        
    def SetChannel(self, slot, source, name):
        # set the data for a slot
        if slot < 0 or slot > 7:
            return False
        
        self.channels[slot] = source
        self.channelNames[slot] = name
        
        return True
    
    def RemoveChannel(self, slot):
        # delete source and name
        if slot < 0 or slot > 7:
            return False
        
        self.channels[slot] = None
        self.channelNames[slot] = ""
        
        return True
    
    def ConnectToScope(self):
        # create the connection window
        config = {}
        config["IP Address"] = GenericIPConfig(init=self.scopeIP).GetConfig()
        config["Scope Port"] = GenericIntConfig(init=self.scopePort, limitMin=1, limitMax=65535).GetConfig()
        
        configWindow = GenericConfigurationWindow(self.master, config, self._OnIPConfigSave)
        configWindow.title("Setup Scope Connection")
        configWindow.wait_window()
        
        # connect to scope
        if self.scopeConnected:
            # already connected, disconnect first
            self.DisconnectFromScope()
        
        try:
            self.scopeSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except Exception as e:
            print (e)
        
        # start send thread
        self.scopeRunThread = True
        self.scopeThread = threading.Thread(target=self._ScopeThread)
        self.scopeThread.start()
        
        return
    
    def DisconnectFromScope(self):
        # remove channels from scope
        for i in range(8):
            if self.channels[i]:
                self._SendChannelInvalidate(i)
        
        # stop thread
        self.scopeRunThread = False
        self.scopeThread.join()
        self.scopeConnected = False
        
        return
    
    def OpenConfigWindow(self, source = None, name = ""):
        # create a subwindow
        self.cWindow = tk.Toplevel(self.master)
        self.cWindow.title("Select or Edit Channel")
        
        # list of variables
        self.listbox = tk.Listbox(self.cWindow, width=50, height=8)
        for i in range(8):
            # insert names into list
            self.listbox.insert(i + 1, "Channel " + str(i + 1) + ": " + self.channelNames[i])
        
        # delete and select button
        deleteButton = tk.Button(self.cWindow, text="Delete", command=self._OnDeleteButton)
        editButton = tk.Button(self.cWindow, text="Edit", command=self._OnEditButton)
        selectButton = tk.Button(self.cWindow, text="Select", command=lambda: self._OnSelectButton(source, name))
        
        if not source:
            selectButton["state"] = tk.DISABLED
        else:
            deleteButton["state"] = tk.DISABLED
            editButton["state"] = tk.DISABLED
        
        self.listbox.grid(row=0, column=0, columnspan=3)
        selectButton.grid(row=1, column=0)
        deleteButton.grid(row=1, column=1)
        editButton.grid(row=1, column=2)
        
        self.cWindow.wait_window()
        
        self.cWindow = None
        
        return
    
    def _OnDeleteButton(self):
        # get selected item and delete from list
        items = self.listbox.curselection()
        for i in items:
            self.RemoveChannel(i)
            self._SendChannelInvalidate(i)
        
        # close the subwindow
        if self.cWindow:
            self.cWindow.destroy()
        
        return
    
    def _OnSelectButton(self, source, name):
        # get selected item and delete from list
        items = self.listbox.curselection()
        for i in items:
            self.SetChannel(i, source, name)
            self._SendChannelConfigData(i)
        
        # close the subwindow
        if self.cWindow:
            self.cWindow.destroy()
        
        return
    
    def _OnEditButton(self):
        # open editor window
        items = self.listbox.curselection()
        slot = -1
        
        for i in items:
            slot = i
        
        if slot < 0:
            return
        
        self.eWindow = tk.Toplevel(self.master)
        self.eWindow.title("Edit Channel " + str(slot))
        
        # string variables for entry fields
        scaleValue = tk.StringVar(self.master, value=str(self.channelScales[slot]))
        offsetValue = tk.StringVar(self.master, value=str(self.channelOffsets[slot]))
        
        scaleLabel = tk.Label(self.eWindow, text="Scale")
        offsetLabel = tk.Label(self.eWindow, text="Offset")
        scaleEntry = tk.Entry(self.eWindow, textvariable=scaleValue)
        offsetEntry = tk.Entry(self.eWindow, textvariable=offsetValue)
        saveButton = tk.Button(self.eWindow, text="OK", command=self._OnSaveButton)
        
        scaleLabel.grid(row=0, column=0)
        offsetLabel.grid(row=1, column=0)
        scaleEntry.grid(row=0, column=1)
        offsetEntry.grid(row=1, column=1)
        saveButton.grid(row=2, column=0, columnspan=2)
        
        self.eWindow.wait_window()
        
        # get text from entries
        try:
            scale = int(scaleValue.get())
            offset = int(offsetValue.get())
            self.channelScales[slot] = scale
            self.channelOffsets[slot] = offset
        
        except Exception as e:
            print (e)
        
        # write new config
        self._SendChannelConfigData(slot)
        
        return
    
    def _ScopeThread(self):
        # task that sends out data
        self.scopeConnected = True
        data =[0] * 8
        
        # send channel configs
        for i in range(8):
            if self.channels[i]:
                print ("Sending channel config data " + str(i))
                self._SendChannelConfigData(i)
        
        while self.scopeRunThread:
            # setup data
            for i in range(8):
                if self.channels[i]:
                    data[i] = int(self.channels[i].GetValue())
                else:
                    data[i] = 0;
            
            # pack and send data
            bytes = struct.pack("<Iiiiiiiii", 17, *data)
            
            #print ("Sending channel data " + str(bytes))
            self.scopeSocket.sendto(bytes, (self.scopeIP, self.scopePort))
            
            time.sleep(0.1)
        
        self.scopeSocket.close()
        self.scopeSocket = None
        self.scopeConnected = False
        
        return
    
    def _SendChannelConfigData(self, slot):
        # send out the channel config data
        if self.scopeSocket:
            channelBytes = struct.pack("<IiI", 32 + slot, self.channelOffsets[slot], self.channelScales[slot])
            configBytes = channelBytes + self.channelNames[slot].encode('utf-8')
            self.scopeSocket.sendto(configBytes, (self.scopeIP, self.scopePort))
        
        return
    
    def _SendChannelInvalidate(self, slot):
        # send a single word
        if self.scopeSocket:
            invBytes = struct.pack("<I", 0x40 + slot)
            self.scopeSocket.sendto(invBytes, (self.scopeIP, self.scopePort))
    
    def _OnIPConfigSave(self, config):
        # store newly entered parameters
        self.scopeIP = config["IP Address"]
        self.scopePort = config["Scope Port"]
        return
    
    def _OnSaveButton(self):
        
        self.eWindow.destroy()
        
        return