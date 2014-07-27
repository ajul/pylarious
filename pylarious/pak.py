import os
import struct
import zlib

HEADER_LENGTH = 21

def readHeader(f):
    """
    Reads a header from an open file f.
    f is assumed to be at the start of the file.
    Returns a tuple
    version, dataOffset, archiveFileCount, fileTableLength, endianness, fileCount
    """
    
    headerBytes = f.read(HEADER_LENGTH)
    
    header = struct.unpack("<LLLL?L", headerBytes)
    
    if header[0] in (7, 9):
        return header
    else:
        raise IOError("PAK version number %d not supported!" % header[0])
        
FILE_RECORD_LENGTH = 272
        
def readFileTable(f, header):
    """
    Reads a file table format from an open file f given a header.
    f is assumed to be at the start of the file table.
    Returns a list of fileRecords. Each fileRecord is a tuple
    path, offset, size, endianness, archiveFileIndex
    """
    version, dataOffset, archiveFileCount, fileTableLength, endianness, fileCount = header
    
    def readFileRecords(f):
        for i in range(fileCount):
            recordBytes = f.read(FILE_RECORD_LENGTH)
            path, offset, size, endianness, archiveFileIndex = struct.unpack("<256sLLLL", recordBytes)
            path, _ = path.decode('ascii').split("\0", 1)
            yield (path, offset, size, endianness, archiveFileIndex)
        
    return list(readFileRecords(f))
    
def unpackArchive(source, filter = None, encoding = None):
    """ 
    Iterates over the files in an archive.
    filter: a function that takes a file record and returns True iff the file is to be unpacked
    """
    
    primaryArchiveFile = open(source, "rb")
    header = readHeader(primaryArchiveFile)
    version, dataOffset, archiveFileCount, fileTableLength, endianness, fileCount = header
    
    # open all other archive files
    archiveFiles = [primaryArchiveFile]
    sourceRoot, sourceExt = os.path.splitext(source)
    for i in range(1, archiveFileCount):
        path = "%s_%d%s" % (sourceRoot, i, sourceExt)
        archiveFiles.append(open(path, "rb"))
        
    fileTable = readFileTable(primaryArchiveFile, header)
    for fileRecord in fileTable:
        path, offset, size, compressedSize, archiveFileIndex = fileRecord
        
        if callable(filter) and not filter(fileRecord): continue
        
        if archiveFileIndex == 0:
            offset += dataOffset
        
        archiveFile = archiveFiles[archiveFileIndex]
        archiveFile.seek(offset)
        
        if compressedSize != 0:
            fileData = zlib.decompress(archiveFile.read(compressedSize))
        else:
            fileData = archiveFile.read(size)
            
        if encoding is not None:
            fileData = fileData.decode(encoding)
        
        print('Extracted file "%s" (%u bytes)' % (path, size))
        yield fileRecord, fileData
        
    for f in archiveFiles:
        f.close()
    
def unpackArchiveToFiles(source, target = None, filter = None):
    """ 
    Unpacks the primary PAK file at source to target directory. If target is not given, it unpacks into the source's directory.
    filter: a function that takes a file record and returns True iff the file is to be unpacked
    """
    if target is None:
        target, _ = os.path.split(source)
    
    for fileRecord, fileData in unpackArchive(source, filter):
        path, offset, size, compressedSize, archiveFileIndex = fileRecord
        
        outPath = os.path.join(target, path)
        outHead, outTail = os.path.split(outPath)
        os.makedirs(outHead, exist_ok = True)
        outFile = open(outPath, "wb")
        outFile.write(fileData)
        outFile.close()
