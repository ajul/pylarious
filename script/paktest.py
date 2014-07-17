import _setpath
import os
import pylarious.pak

def filterStats(fileRecord):
    return "Public/Main/Stats" in fileRecord[0]

source = "D:/Steam/steamapps/common/Divinity - Original Sin/Data/Main.pak"

pylarious.pak.unpack(source, "out/extract", filter = filterStats)
