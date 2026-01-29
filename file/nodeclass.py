from network.payloads.gridelementconfigs.nodeconfig import NodeConfig
from auxillary.typeinfo import *

class Node:
    def __init__(self, id, connectedPoints, type):
        # store paramters
        self.id = id
        self.connectedPoints = connectedPoints
        self.type = type
        
        # update node for every point
        for p in connectedPoints:
            p.nodeId = self.id
    
    def CreateNodeGridConfiguration(self):
        # get type representation
        type = GetTypeID(self.type)
        return NodeConfig(nodeType=type, id=self.id, rsvd=0)
    
    @staticmethod
    def CreateNodeFromGridConfiguration(config):
        id = config.id
        type = GetTypeFromID(config.nodeType)
        
        return Node(id, [], type)