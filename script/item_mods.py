import _setpath
import os
import pylarious.stats

statDir = "out/extract/Public/Main/Stats/Generated/"

def getModData(entry):
    value = (entry.getData("Value") or ["0"])[0]
    effect = ""
    for k, v in sorted(entry.data.items()):
        if k in ("Value", "Damage Type"): continue
        elif k == "Flags":
            for flag in v:
                effect += "* %s\n" % flag
        elif k == "DamageFromBase":
            effect += "* %s%% extra damage as %s\n" % (v, entry.getData("Damage Type")[0])
        elif k == "ExtraProperties":
            status, chance, duration = v.split(",")
            effect += "* %s%% chance to apply %s for %s turns\n" % (chance, status, duration)
        elif k in ("Air", "Earth", "Fire", "Water", "Poison", "Shadow"):
            effect += "* %s%% %s resistance\n" % (int(v) * 5 - 5, k)
        elif k == "Shield":
            effect += "* %s%% chance to block\n" % v[0]
        else:
            if k in ("DamageBoost", "CriticalChance"):
                effect += "* %s%% %s\n" % (v, k)
            else:
                effect += "* %s %s\n" % (v, k)
    return value, effect

itemFiles = [
    os.path.join(statDir, "Data/Armor.txt"),
    os.path.join(statDir, "Data/Shield.txt"),
    os.path.join(statDir, "Data/Weapon.txt"),
    ]

itemData = {}

for file in itemFiles:
    f = open(file)
    itemData.update(pylarious.stats.parseEntries(f))
    f.close()

f = open(os.path.join(statDir, "DeltaModifier.txt"))
deltamods = pylarious.stats.parseDeltamods(f)
f.close()

armorTable = '{|class = "wikitable sortable"\n'
armorTable += '! Internal name !! Affixes !! Slot !! Armor Type !! Boost Type !! Value !! Effect\n'


# armor mods
for internalName, deltamod in deltamods.items():
    if deltamod.getParam("ModifierType") == "Armor":
        totalValue = 0
        totalEffect = ""
        for boost in deltamod.boosts:
            value, effect = getModData(itemData[boost])
            totalValue += int(value)
            totalEffect += effect
        armorTable += "|- \n"
        armorTable += "| %s \n" % internalName
        armorTable += "| %s \n" % deltamod.affixString()
        armorTable += "| %s \n" % (deltamod.getParam("SlotType") or "Any")
        armorTable += "| %s \n" % (deltamod.getParam("ArmorType") or "Any")
        armorTable += "| %s \n" % (deltamod.getParam("BoostType") or "")
        armorTable += "| %d \n" % totalValue
        armorTable += "| \n%s" % totalEffect
armorTable += "|}"

shieldTable = '{|class = "wikitable sortable"\n'
shieldTable += '! Internal name !! Affixes !! Boost Type !! Value !! Effect\n'

# shield mods
for internalName, deltamod in deltamods.items():
    if deltamod.getParam("ModifierType") == "Shield":
        totalValue = 0
        totalEffect = ""
        for boost in deltamod.boosts:
            value, effect = getModData(itemData[boost])
            totalValue += int(value)
            totalEffect += effect
        shieldTable += "|- \n"
        shieldTable += "| %s \n" % internalName
        shieldTable += "| %s \n" % deltamod.affixString()
        shieldTable += "| %s \n" % (deltamod.getParam("BoostType") or "")
        shieldTable += "| %d \n" % totalValue
        shieldTable += "| \n%s" % totalEffect
shieldTable += "|}"

weaponTable = '{|class = "wikitable sortable"\n'
weaponTable += '! Internal name !! Affixes !! Weapon Type !! Boost Type !! Value !! Effect\n'

# weapon mods
for internalName, deltamod in deltamods.items():
    if deltamod.getParam("ModifierType") == "Weapon":
        totalValue = 0
        totalEffect = ""
        for boost in deltamod.boosts:
            value, effect = getModData(itemData[boost])
            totalValue += int(value)
            totalEffect += effect
        weaponTable += "|- \n"
        weaponTable += "| %s \n" % internalName
        weaponTable += "| %s \n" % deltamod.affixString()
        weaponTable += "| %s \n" % (deltamod.getParam("WeaponType") or "Any")
        weaponTable += "| %s \n" % (deltamod.getParam("BoostType") or "")
        weaponTable += "| %d \n" % totalValue
        weaponTable += "| \n%s" % totalEffect
weaponTable += "|}"

print(weaponTable)
