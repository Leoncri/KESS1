import threading

class PacketDistributor:
    def __init__(self, name = ""):
        # dictionary for ongoing transfers
        self.transferLockDict = dict()
        self.transferDataDict = dict()
        
        self.multipleTransferLockDict = dict()
        self.multipleTransferDataDict = dict()
        
        self.name = name
    
    def RegisterTransfer(self, id : int):
        # return False if id is already in dict
        if id in self.transferLockDict:
            return False
        
        # create condition varaible and store
        self.transferLockDict[id] = threading.Condition(threading.Lock())
        
        return
    
    def RegisterMultipleTransfers(self, id : int):
        # return False if id is already in dict
        if id in self.multipleTransferLockDict:
            return False
        
        # create condition varaible and store
        self.multipleTransferLockDict[id] = threading.Condition(threading.Lock())
        
        return
    
    def WaitForTransferComplete(self, id : int):
        # wait for the transaction to get a respond
        with self.transferLockDict[id]:
            self.transferLockDict[id].wait_for(lambda: self.IsDataAvailable(id), timeout = 1)
        
        # remove lock from dictionary
        self.transferLockDict.pop(id, None)
        
        # return data
        return self.transferDataDict.pop(id, None)
    
    def WaitForMultipleTransfersComplete(self, id : int, packets : int):
        # setup transaction data
        self.multipleTransferDataDict[id] = []
        
        # wait for multiple transactions to get a respond
        with self.multipleTransferLockDict[id]:
            self.multipleTransferLockDict[id].wait_for(lambda: self.IsMultipleDataAvialable(id, packets), timeout = 1)
        
        # remove lock from dictionary
        self.multipleTransferLockDict.pop(id, None)
        
        # only return number fo available packets
        return self.multipleTransferDataDict.pop(id, None)
    
    def NewPacketData(self, id : int, data : bytearray):
        # check if id is registered
        if not id in self.transferLockDict:
            if not id in self.multipleTransferLockDict:
                print (self.name + ": Data incoming without transfer, ID = " + str(id))
                return
            else:
                # store data in multiple data dict
                self.multipleTransferDataDict[id].append(data)
                with self.multipleTransferLockDict[id]:
                    self.multipleTransferLockDict[id].notify_all()
        else:
            # store data
            self.transferDataDict[id] = data
            
            with self.transferLockDict[id]:
                self.transferLockDict[id].notify_all()
        
        return
    
    def IsDataAvailable(self, id : int):
        # check if data is available
        if id in self.transferDataDict:
            return True
        return False
    
    def IsMultipleDataAvialable(self, id : int, packets : int):
        # check if data is available and length matches
        if id in self.multipleTransferLockDict:
            if len(self.multipleTransferDataDict[id]) == packets:
                return True
        return False