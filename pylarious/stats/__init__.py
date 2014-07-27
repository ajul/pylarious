import re
from pylarious.stats.deltamod import *
from pylarious.stats.entry import *

def tokenize(line):
    for match in re.finditer('"(.*?)"|(\S+)', line):
        yield match.group(match.lastindex)
