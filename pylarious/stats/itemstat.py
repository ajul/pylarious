from pylarious.stats import tokenize

class ItemStat():
    def __init__(self, s):
        (
        self.internalName, 
        self.key, 
        _,
        _,
        _,
        self.objectCategory,
        self.minAmount,
        self.maxAmount,
        self.priority,
        self.unique,
        self.minLevel,
        self.maxLevel,
        ) = s.split(',')
        
        self.internalName = self.internalName[1:-1]
        self.key = self.key[1:-1]
        self.objectCategory = self.objectCategory[1:-1]
        
        self.minAmount = int(self.minAmount)
        self.maxAmount = int(self.maxAmount)
        self.priority = int(self.priority)
        self.minLevel = int(self.minLevel)
        self.maxLevel = int(self.maxLevel)
        
        self.unique = bool(int(self.unique))
        
    def hasNonUnitAmount(self):
        return self.minAmount != 1 or self.maxAmount != 1
        
def parseItemStats(lines):
    result = {}
    for lineno, line in enumerate(lines):
        tokens = list(tokenize(line))
        if len(tokens) == 0: continue
        if tokens[0] == "object" and tokens[1] == "itemstat":
            itemStat = ItemStat(tokens[2])
            result[itemStat.internalName] = itemStat
    return result