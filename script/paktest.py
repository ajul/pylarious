import _setpath
import os
import pylarious.pak

source = "D:/Steam/steamapps/common/Divinity - Original Sin/Data/Main.pak"

pylarious.pak.unpack(source, "out/", lambda x: "Public/Main/Stats" in x[0])
