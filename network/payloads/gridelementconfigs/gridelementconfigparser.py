import struct

from network.packetsegment import PacketSegment
from network.payloads.gridelementconfigs import *
from network.payloads.gridelementconfigs.scibreakbreakerconfig import *

class GridElementConfigParser:
    @staticmethod
    def GetPayloadFromBytes(payloadBytes : bytearray,
        numberElements : int) -> list[GridElementConfig]:
        """Retrieves all GridElementConfigs from binary data.
        
        Args:
            payloadBytes (bytearray): Binary data of the entire payload
                (including padding)
            numberElements (int): Number of GridElementConfigs in the binary
                data.
        Returns:
            A list of GridElementConfig. The order of occurence is maintained.
        """

        # remove zero bytes at the end used for padding
        numberBytesUsed = GridElementConfig.maxTotalSize * numberElements
        unpaddedPayloadBytes = payloadBytes[:numberBytesUsed]

        gridElementConfigChunks = GridElementConfigParser._SplitIntoChunks(
            unpaddedPayloadBytes, numberElements)
        
        # convert each bytearray into GridElementConfig
        gridElementConfigs = list(map(GridElementConfigParser._GetGridElementConfig,
            gridElementConfigChunks))
        return gridElementConfigs

    @staticmethod
    def _SplitIntoChunks(array: bytearray, chunks : int) -> list[bytearray]:
        """Splits a bytearray in equally sized parts.

        If slicing the array in equal parts isn't possible an exception
        is raised.
        
        Args:
            array (bytearray): Array, which shall be splitted
            chunks (int): Number of equally sized parts

        Returns:
            List of bytearrays, which all have the length chunk
        
        Raises:
            struct.error: array is either to big or to small.
            IndexError: array cannot be equally splitted.
        """
        print (len(array))
        print (chunks)
        if len(array) % chunks != 0:
            raise IndexError("Error: Equally sized parts are not possible")
        chunkSize = len(array) // chunks
        singleConfigFormatString = str(chunkSize) + "s"
        formatString = (PacketSegment._byteOrder +
            singleConfigFormatString * chunks)

        chunksTuple = struct.unpack(formatString, array)
        chunks = list(chunksTuple)

        return chunks

    @staticmethod
    def _GetGridElementConfig(nodeConfigBytes : bytearray) -> NodeConfig:
        """Creates the fitting grid element config from binary data for
        a single GridElementConfig.

        No tests are performed to validate, the binary data is a grid element
            config (e.g. Node, Point, Segment, Converter, ...)

        Args:
            nodeConfigBytes (bytearray): The binary data consists of:
                1. ElementType (uint16)
                2. grid element config (variable in size; further bytes are
                    ignored)
        Returns:
            A NodeConfig (or a derived class) based upon the binary data.

        Raises:
            IndexError: The number of bytes is either insufficient to determine the
                ElementType or to retrieve the proper GridElementConfig.
        """
        if len(nodeConfigBytes) < 2:
            raise IndexError("""Error: Insufficient number of bytes to determine
                the type of the grid element config.""")
        # parse type of config element
        typeBytes = nodeConfigBytes[:2]
        typeFullFormatString = PacketSegment._byteOrder + "H"
        (elementType, ) = struct.unpack(typeFullFormatString, typeBytes)

        if elementType == ElementType.NODE:
            payload = NodeConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.POINT:
            payload = PointConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.SEGMENT:
            payload = SegmentConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.CONVERTER:
            payload = ConverterConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.BREAKER:
            payload = BreakerConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.FENSWITCHGEAR:
            payload = FENSwitchgearConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.SOURCE:
            payload = SourceConfig.GetPayloadFromBytes(nodeConfigBytes)
        elif elementType == ElementType.SCIBREAKBREAKER:
            payload = SciBreakBreakerConfig.GetPayloadFromBytes(nodeConfigBytes)
        else:
            payload = None
        return payload