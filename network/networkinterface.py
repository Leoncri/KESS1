import socket
import threading
import time
from network.headers.header import *
from network.packets.isalive import *
import tkinter as tk
from generic.genericconfigwindowclass import *
from network.packets.packetparser import *

class NetworkInterface:
    def __init__(self, editor):
        # parameters
        self.editor = editor
        self.gridFile = None
        
        # set some variables
        self.runThreads = False
        self.socket = None
        self.sendLock = threading.Lock()
        self.timeoutLock = threading.Lock()
        self.statusLock = threading.Lock()
        
        self.ip = "127.0.0.1"
        self.port = 50000
        
        # recv and periodic task
        self.recvTask = None
        self.periodicTask = None
        self.timeoutCounter = 0
        
        # status of the interface
        self.interfaceStatus = "not connected"
    
    def SetGridFile(self, gridFile):
        self.gridFile = gridFile
        return
    
    def ConnectToServer(self, master):
        # create a generic configuration window
        config = {}
        config["IP Address"] = GenericIPConfig(init=self.ip).GetConfig()
        config["Server Port"] = GenericIntConfig(init=self.port, limitMin=1, limitMax=65535).GetConfig()
        
        configWindow = GenericConfigurationWindow(master, config, self._OnIPConfigSave)
        configWindow.title("Setup Network Configuration")
        configWindow.wait_window()
        
        # check if we can connect to a server
        if self.socket != None:
            return False
        
        # create a socket and connect to the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        
        try:
            self.socket.connect((self.ip, self.port))
        except Exception as e:
            #print (e)
            #print ("Cannot create server connection")
            self.socket.close()
            self.socket = None
            return False
        
        
        # start the recv thread
        self.runThreads = True
        self.recvTask = threading.Thread(target=self._RecvThreadFunction)
        self.recvTask.start()
        
        # start the periodic task
        self.periodicTask = threading.Thread(target=self._PeriodicThreadFunction)
        self.periodicTask.start()
        
        self.SetStatus("connected")
        
        return True
    
    def Disconnect(self):
        # disconnect from server        
        # check if we need to disconnect
        if not self.IsConnected():
            return
            
        self.SetStatus("not connected")
        
        # stop recv and periodic task
        print ("Stopping network threads")
        self.runThreads = False
        
        # join both tasks
        try:
            self.recvTask.join()
        except:
            pass
        self.recvTask = None
        print ("Recv task ended")
        
        try:
            self.periodicTask.join()
        except Exception as e:
            pass
        self.periodicTask = None
        print ("Periodic task ended")
        
        self.socket.close()
        self.socket = None
        
        
        
        return
    
    def SendData(self, data : bytearray):
        # get lock and send out data
        self.sendLock.acquire()
        
        # send out data
        try:
            self.socket.sendall(data)
        except:
            pass
        
        # release lock and return
        self.sendLock.release()
        return
    
    def SetStatus(self, status):
        # get lock and set status
        self.statusLock.acquire()
        
        self.interfaceStatus = status
        
        self.statusLock.release()
        
        # notify editor
        self.editor.ChangedNetworkStatus()
        
        return
    
    def IsConnected(self):
        # return if interface is connected
        return self.interfaceStatus == "connected"
    
    def _RecvThreadFunction(self):
        # some variables
        bytesToRead = 0
        counter = 0
        
        # main loop
        while self.runThreads:
            # read in 16 bytes as header
            bytesToRead = 8
            header = bytearray()
            payload = bytearray()
            counter += 1
            #print ("Recv thread loop: " + str(counter))
            
            try:
                #print ("Reading in header")
                header = self._RecvBytes(bytesToRead)
                #print ("Header read in")
            except Exception as e:
                print ("Exception for reading in header: " + str(e))
                header = None
            
            #print (header)
            
            # reset timeout counter
            self.timeoutLock.acquire()
            self.timeoutCounter = 0
            self.timeoutLock.release()
            
            if header:
                # process the header and get the number of bytes to be read as payload
                payloadLength = self._GetPacketLength(header) - 8
                #print (payloadLength)
            
                try:
                    #print ("Reading in payload")
                    payload = self._RecvBytes(payloadLength)
                    #print ("Payload read in")
                except Exception as e:
                    print ("Exception for reading in payload: " + str(e))
                    payload = None
                
                #print (payload)
                
                if not payload:
                    continue
                
                #print ("Forwarding packet")
                # send header and payload to device
                self._ForwardPacketData(header, payload)
                #print ("Packet forwarded")
                #print ("Entering next recv loop")
        
        print ("Recv function left")
        # loop breaks
        self.runThreads = False
        
        self.Disconnect()
        
        return
    
    def _PeriodicThreadFunction(self):
        # periodic thread sends isAlive packet every 1 s
        while self.runThreads:
            # set timeout counter
            self.timeoutLock.acquire()
            self.timeoutCounter = 1
            self.timeoutLock.release()
            
            # send packet
            self._SendIsAlivePacket()
            
            # wait 1 s
            time.sleep(2)
            
            # check if the timeout signal was reset
            if self.timeoutCounter != 0:
                self.runThreads = False
        
        # when this function breaks, server connection was interrrupted
        self.Disconnect()
        
        return
    
    def _RecvBytes(self, length):
        # receive a certain length of bytes
        recvData = bytearray()
        while length > 0:
            try:
                data = self.socket.recv(length)
            except:
                raise ConnectionError
                
            length -= len(data)
            recvData += data
        
        return recvData
    
    def _GetPacketLength(self, header : bytearray) -> int:
        # stuff header into header class and get data
        type, device, id, length, connection = Header.ParseBytes(header)
        
        return length
    
    def _ForwardPacketData(self, header, payload):
        # process header
        packet = PacketParser.GetPacketFromBytes(header + payload)
        #print (packet)
        
        # check type
        if isinstance(packet, IsAlivePacket):
            # TODO
            #print ("Incoming IsAlive packet")
            pass
        else:
            # send packets for grid file to class
            if packet.header.deviceType == DeviceType.GRID:
                self.gridFile.NewPacket(packet)
            else:
                self.editor.NewPacket(packet)
                
        return
    
    def _SendIsAlivePacket(self):
        # send out data
        self.SendData(IsAlivePacket.FromConfig().GetBytes())
        
        return
    
    def _OnIPConfigSave(self, config):
        # store newly entered parameters
        self.ip = config["IP Address"]
        self.port = config["Server Port"]
        return