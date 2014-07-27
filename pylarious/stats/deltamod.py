from pylarious.stats import tokenize

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