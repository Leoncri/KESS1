from network.packetsegment import PacketSegment
from network.headers.header import *
from network.headers.commandrespond import CommandRespondHeader
from network.headers.gridcommand import GridCommandLoadFileHeader
from network.headers.gridrespond import GridCommandGetFileHeader
from network.headers.gridrespond import GridRespond
from network.headers.devicedata import *

class HeaderParser:
    """Collection of methods to retrieve a Header from binary data.

    Typical usage:
        header = HeaderParser.GetHeaderFromBytes(packetBytes)

    TODO:
    - split GetHeaderFromBytes into smaller functions
    - enhance error handling on this level (is the packet corrupted?)
    
    """
    @staticmethod
    def GetHeaderFromBytes(packetBytes: bytearray) -> tuple[Header, int]:
        """Retrieves a header from a packet in binary form.

        Args:
            packetBytes (bytearray): The bytes, the header shall be
            created from. Further attached data in byte form (e.g. the payload)
            will be ignored.
            
        Returns:
            A tuple (header, lastByte) where header is the retrieved header (or
            a subclass) and lastByte is the index of the last used byte.

        Raises:
            IndexError: The number of bytes is insufficient for the anticipated
                header.
        """
        headerStart = 0
        headerEnd = Header.size

        # slice and parse the general header
        headerBytes = packetBytes[headerStart : headerEnd]
        (packetType, deviceType, deviceId, length, connection) = (Header.ParseBytes(headerBytes))

        if packetType == PacketType.RESPOND:
            # slice and parse the command respond header
            (headerStart, headerEnd) = PacketSegment.UpdateSlicingIndices(headerStart, headerEnd, CommandRespondHeader.size)
            
            commandRespondHeaderBytes = packetBytes[headerStart : headerEnd]
            (result, commandId) = CommandRespondHeader.ParseBytes(commandRespondHeaderBytes)

            if deviceType == DeviceType.GRID:
                # either normal respond packet OR grid data respond
                if result == GridRespond.GET_CONFIG_DATA:
                    # create a config data packet
                    # align and get additional data from payload
                    (headerStart, headerEnd) = PacketSegment.UpdateSlicingIndices(headerStart, headerEnd, GridCommandGetFileHeader.size)
                    getFileHeaderBytes = packetBytes[headerStart : headerEnd]
                    
                    # get version from payload
                    (version, subversion, totalParts, part, length) = GridCommandLoadFileHeader.ParseBytes(getFileHeaderBytes)
                    
                    # create header
                    header = GridCommandGetFileHeader(deviceId, length, connection, result, commandId, version, subversion, totalParts, part, length)
                
                else:
                    # create a normal command respond header
                    header = CommandRespondHeader(deviceType, deviceId, length, connection, result, commandId)
            
            elif deviceType == DeviceType.SERVER:
                # either normal respond pacekt or server status, both use command respond header
                header = CommandRespondHeader(deviceType, deviceId, length, connection, result, commandId)
            
            else:
                header = CommandRespondHeader(deviceType, deviceId, length, connection, result, commandId)
        
        elif packetType == PacketType.DEVICEDATA:
            # update the header end
            (headerStart, headerEnd) = PacketSegment.UpdateSlicingIndices(headerStart, headerEnd, DeviceDataHeader.size)
            
            deviceDataHeaderBytes = packetBytes[headerStart : headerEnd]
            id, _ = DeviceDataHeader.ParseBytes(deviceDataHeaderBytes)
            
            header = DeviceDataHeader(deviceType, deviceId, length, connection, id)
            
        elif packetType == PacketType.ISALIVE:
            header = Header(packetType, deviceType, deviceId, length, connection)
        
        else:
            raise Exception(f"Unkown type: {packetType}")
        
        return (header, headerEnd)