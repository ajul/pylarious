import _setpath
import os
import pylarious.stats

statDir = "out/extract/Public/Main/Stats/Generated/"

files = [
    os.path.join(statDir, "Links/Armor.txt"),
    os.path.join(statDir, "Links/Object.txt"),
    os.path.join(statDir, "Links/Potion.txt"),
    os.path.join(statDir, "Links/Shield.txt"),
    os.path.join(statDir, "Links/Weapon.txt"),
    ]
    
data = {}

for file in files:
    f = open(file)
    data.update(pylarious.stats.parseItemStats(f))
    f.close()

result = '<table class="wikitable sortable mw-collapsible mw-collapsed">\n'
result += '    <tr>\n'
result += '        <th>Internal name</th>\n'
result += '        <th>Object category</th>\n'
result += '        <th>Min amount</th>\n'
result += '        <th>Max amount</th>\n'
result += '    </tr>\n'

for name, stats in sorted(data.items()):
    if stats.minAmount < 0 or stats.maxAmount < 0: continue
    result += '    <tr>\n'
    result += '        <td>%s</td>\n' % name
    result += '        <td>%s</td>\n' % stats.objectCategory
    result += '        <td>%d</td>\n' % stats.minAmount
    result += '        <td>%d</td>\n' % stats.maxAmount
    result += '    </tr>\n'

result += '</table>\n'

print(result)
