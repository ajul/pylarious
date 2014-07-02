import _setpath
import pylarious.pak

f = open("D:/Steam/steamapps/common/Divinity - Original Sin/Data/Engine.pak", 'rb')
header = pylarious.pak.readHeader(f)
fileTable = pylarious.pak.readFileTable(f, header)
for record in fileTable:
    path, offset, size, unknown, archiveFileIndex = record
    print(path, "%x" % size)
