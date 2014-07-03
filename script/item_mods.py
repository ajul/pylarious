import _setpath
import os
import pylarious.stats

source = "out/extract/Public/Main/Stats/Generated/Data/Shield.txt"

f = open(source)
weapons = pylarious.stats.parse(f)
f.close()

s = ""
for internalName, weapon in sorted(weapons.items()):
    if weapons["_BOOSTS_Shield"] in weapon.usingList:
        s += "|-\n"
        s += "| %s \n" % internalName
        s += "| %s \n" % (weapon.getData("Value") or ["0"])[0]
        s += "| \n"
        for k, v in sorted(weapon.data.items()):
            if k in ("Value", "Damage Type"): continue
            elif k == "Flags":
                for flag in v:
                    s += "* %s\n" % flag
            elif k == "DamageFromBase":
                s += "* %s%% extra damage as %s\n" % (v[0], weapon.getData("Damage Type")[0])
            elif k == "ExtraProperties":
                s += "* %s%% chance to apply %s for %s turns\n" % (v[1], v[0], v[2])
            elif k in ("Air", "Earth", "Fire", "Water", "Poison", "Shadow"):
                s += "* %s%% %s resistance\n" % (v[0], k)
            elif k == "Shield":
                s += "* +%s%% chance to block\n" % v[0]
            else:
                if k in ("DamageBoost", "CriticalChance"):
                    s += "* +%s%% %s\n" % (v[0], k)
                else:
                    s += "* +%s %s\n" % (v[0], k)

print(s)
        
