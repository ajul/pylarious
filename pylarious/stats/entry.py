from pylarious.stats import tokenize

class Entry():
    def __init__(self, internalName):
        self.internalName = internalName
        self.data = {}
        self.usingList = []
        self.type = None
        
    def using(self, other):
        self.usingList.append(other)
        
    def getData(self, key):
        if key in self.data.keys():
            return self.data[key]
        else:
            for other in self.usingList:
                result = other.getData(key)
                if result is not None: return result
        return None
        
    def getAllData(self):
        result = {}
        for other in reversed(self.usingList):
            result.update(other.getAllData())
        result.update(self.data)
        return result

def parseEntries(lines):
    result = {}
    for lineno, line in enumerate(lines):
        tokens = list(tokenize(line))
        if len(tokens) == 0: continue
        if tokens[0] == "new":
            if tokens[1] == "entry":
                internalName = tokens[2]
                entry = Entry(internalName)
                result[internalName] = entry
        elif tokens[0] == "type":
            entry.type = tokens[1]
        elif tokens[0] == "using":
            entry.using(result[tokens[1]])
        elif tokens[0] == "data":
            entry.data[tokens[1]] = tokens[2]
    return result