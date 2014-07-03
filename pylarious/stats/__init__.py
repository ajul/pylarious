import re

class Entry():
    def __init__(self, internalName):
        self.internalName = internalName
        self.data = {}
        self.usingList = []
        
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

def parse(lines):
    result = {}
    for lineno, line in enumerate(lines):
        tokens = list(tokenize(line))
        if len(tokens) == 0: continue
        if tokens[0] == "new":
            if tokens[1] != "entry": raise ParseError('Expected "entry" after "new"!')
            internalName = tokens[2]
            entry = Entry(internalName)
            result[internalName] = entry
        elif tokens[0] == "type":
            continue #TODO
        elif tokens[0] == "using":
            entry.using(result[tokens[1]])
        elif tokens[0] == "data":
            entry.data[tokens[1]] = tokens[2].split(',')
        else:
            raise ParseError('Unrecognized initial token "%s"!' % tokens[0])
    return result
            

def tokenize(line):
    for match in re.finditer('"(.*?)"|(\S+)', line):
        yield match.group(match.lastindex)
