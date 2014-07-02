import os
import struct

HEADER_LENGTH = 21

def readHeader(f):
    """
    # version, dataOffset, archiveFileCount, fileTableLength, unknown, fileCount
    """
    
    headerBytes = f.read(HEADER_LENGTH)
    
    header = struct.unpack("<LLLL?L", headerBytes)
    
    if header[0] == 7:
        return header
    else:
        raise IOError("PAK version number %d not supported!" % header[0])
        
FILE_RECORD_LENGTH = 272
        
def readFileTable(f, header):
    version, dataOffset, archiveFileCount, fileTableLength, unknown, fileCount = header
    
    def readFileRecords(f):
        for i in range(fileCount):
            recordBytes = f.read(FILE_RECORD_LENGTH)
            path, offset, size, unknown, archiveFileIndex = struct.unpack("<256sLLLL", recordBytes)
            path, _ = path.decode('ascii').split("\0", 1)
            yield (path, offset, size, unknown, archiveFileIndex)
        
    return list(readFileRecords(f))
    
def unpack(path):
    pass
