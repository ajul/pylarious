import _setpath
import os
import pylarious.stats

statDir = "out/extract/Public/Main/Stats/Generated/"

itemFiles = [
    os.path.join(statDir, "Data/Armor.txt"),
    os.path.join(statDir, "Data/Shield.txt"),
    os.path.join(statDir, "Data/SkillData.txt"),
    os.path.join(statDir, "Data/Weapon.txt"),
    ]

itemData = {}

for file in itemFiles:
    f = open(file)
    itemData.update(pylarious.stats.parseEntries(f))
    f.close()

armorTable = '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
armorTable += '! Internal name !! Requirements !! Slot !! Armour type !! Armour rating !! Durability !! Bonuses \n'

# armor mods
for internalName, item in itemData.items():
    if item.getData("InventoryTab") != "Equipment": continue
    if item.type == "Armor":
        armorTable += "|- \n"
        armorTable += "| %s \n" % internalName
        armorTable += "| %s \n" % (item.getData("Requirements") or "")
        armorTable += "| %s \n" % item.getData("Slot")
        armorTable += "| %s \n" % (item.getData("ArmorType") or "")
        armorTable += "| %s \n" % item.getData("Armor Defense Value")
        armorTable += "| %d \n" % (int(item.getData("Durability") or "0") * 10)

        armorTable += "| "
        hasBoost = False
        for k, v in sorted(item.getAllData().items()):
            if k in ("Requirements", "Slot", "ArmorType", "Armor Defense Value", "Durability", "DurabilityDegradeSpeed", "Weight",
                     "InventoryTab", "ComboCategory", "ModifierType", "ItemColor", "Value",
                     "Act", "Act part"): continue
            if v == "0": continue
            hasBoost = True
            if k in ("Air", "Earth", "Fire", "Water", "Poison", "Shadow"):
                armorTable += "%d%% %s resistance" % (5 * int(v), k)
            else:
                armorTable += "%s %s" % (v, k)
            armorTable += "<br/>"
        if hasBoost:
            armorTable = armorTable[:-5]
        armorTable += "\n"
armorTable += "|}"

shieldTable = '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
shieldTable += '! Internal name !! Requirements !! Blocking !! Movement !! Durability \n'

# shield mods
for internalName, item in itemData.items():
    if item.getData("InventoryTab") != "Equipment": continue
    if item.type == "Shield":
        shieldTable += "|- \n"
        shieldTable += "| %s \n" % internalName
        shieldTable += "| %s \n" % (item.getData("Requirements") or "")
        shieldTable += "| %s \n" % item.getData("Blocking")
        shieldTable += "| %s \n" % (item.getData("Movement") or "")
        shieldTable += "| %d \n" % (int(item.getData("Durability") or "0") * 10)
shieldTable += "|}"

weaponTable = '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
weaponTable += '! Internal name !! Requirements !! Weapon type !! AP Cost !! Damage !! Damage Range !! Damage Boost !! Damage Type '
weaponTable += '!! Critical Chance !! Critical Damage !! Durability \n'

# weapon mods
for internalName, item in itemData.items():
    if item.getData("InventoryTab") != "Equipment": continue
    if item.type == "Weapon":
        weaponTable += "|- \n"
        weaponTable += "| %s \n" % internalName
        weaponTable += "| %s \n" % item.getData("Requirements")
        weaponTable += "| %sH %s \n" % (item.getData("Handedness"), item.getData("WeaponType"))
        weaponTable += "| %s \n" % item.getData("AttackAPCost")
        weaponTable += "| %s \n" % item.getData("Damage")
        weaponTable += "| %s \n" % item.getData("Damage Range")
        weaponTable += "| %d%% \n" % int(item.getData("DamageBoost") or "0")
        weaponTable += "| %s \n" % item.getData("Damage Type")
        weaponTable += "| %s \n" % item.getData("CriticalChance")
        weaponTable += "| x%0.1f \n" % (1.0 + float(item.getData("CriticalDamage")) * 0.5)
        weaponTable += "| %d \n" % (int(item.getData("Durability") or "0") * 10)
weaponTable += "|}"

skillTable = '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
skillTable += '! Internal name !! AP Cost !! Damage !! Damage Multiplier !! Damage Range\n'

# skills
for internalName, item in itemData.items():
    if item.getData("Damage") is None or item.getData("Damage") == "0": continue
    if item.getData("Level") is not None: continue
    if item.getData("Skillbook") is None: continue
    if "Enemy" in internalName: continue
    if item.type == "SkillData":
        skillTable += "|- \n"
        skillTable += "| %s \n" % internalName
        skillTable += "| %s \n" % item.getData("ActionPoints")
        skillTable += "| %s \n" % item.getData("Damage")
        skillTable += "| %s \n" % item.getData("Damage Multiplier")
        skillTable += "| %s \n" % item.getData("Damage Range")
skillTable += "|}"

print(armorTable)
