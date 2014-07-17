import re

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
    
class Deltamod():
    def __init__(self, internalName):
        self.internalName = internalName
        self.params = {}
        self.boosts = []
        self.affixes = []
        
    def addBoost(self, boost):
        self.boosts.append(boost)
        
    def addAffix(self, affix):
        self.affixes.append(affix)
        
    def affixString(self):
        result = ""
        for affix in self.affixes:
            result += "%s, " % affix
        return result[:-2]
        
    def getParam(self, key):
        if key in self.params: return self.params[key]
        return None
    
def parseDeltamods(lines):
    result = {}
    for lineno, line in enumerate(lines):
        tokens = list(tokenize(line))
        if len(tokens) == 0: continue
        if tokens[0] == "new":
            if tokens[1] == "deltamod":
                deltamod = Deltamod(tokens[2])
                result[tokens[2]] = deltamod
            elif tokens[1] == "boost":
                deltamod.addBoost(tokens[2].split(",")[0])
        elif tokens[0] in ("prefixname", "suffixname"):
            deltamod.addAffix(tokens[1])
        elif tokens[0] == "param":
            deltamod.params[tokens[1]] = tokens[2]
            
    return result

def tokenize(line):
    for match in re.finditer('"(.*?)"|(\S+)', line):
        yield match.group(match.lastindex)
