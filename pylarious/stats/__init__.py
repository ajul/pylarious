import re

def tokenize(line):
    for match in re.finditer(r'("(.*?)"|([^"\s]+))+', line):
        # print(match.group(0))
        yield match.group(0)

from pylarious.stats.deltamod import *
from pylarious.stats.itemstat import *
from pylarious.stats.entry import *