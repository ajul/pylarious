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
    
def unpack(source, target = None, filter = None):
    """ 
    filter: a function that takes a file record and returns True iff the file is to be unpacked.
    """
    if target is None:
        target, _ = os.path.split(source)
    
    primaryArchiveFile = open(source, "rb")
    header = readHeader(primaryArchiveFile)
    version, dataOffset, archiveFileCount, fileTableLength, headerUnkown, fileCount = header
    
    # open all other archive files
    archiveFiles = [primaryArchiveFile]
    sourceRoot, sourceExt = os.path.splitext(source)
    for i in range(1, archiveFileCount):
        path = "%s_%d%s" % (sourceRoot, i, sourceExt)
        archiveFiles.append(open(path, "rb"))
        
    fileTable = readFileTable(primaryArchiveFile, header)
    for fileRecord in fileTable:
        if filter is not None and not filter(fileRecord): continue
        path, offset, size, unknown, archiveFileIndex = fileRecord
        
        if archiveFileIndex == 0:
            offset += dataOffset
        
        archiveFile = archiveFiles[archiveFileIndex]
        archiveFile.seek(offset)
        fileData = archiveFile.read(size)
        
        outPath = os.path.join(target, path)
        outHead, outTail = os.path.split(outPath)
        os.makedirs(outHead, exist_ok = True)
        outFile = open(outPath, "wb")
        outFile.write(fileData)
        outFile.close()
        
        print('Extracted file "%s" (%u bytes)' % (path, size))
        
    for f in archiveFiles:
        f.close()
