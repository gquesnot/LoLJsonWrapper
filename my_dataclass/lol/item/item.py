from dataclasses import dataclass, field, asdict
from typing import Dict, Any

from dacite import from_dict


@dataclass
class Item:
    name: str
    id: int
    hp: float = field(default=0)
    gold: int = field(default=0)
    hpregen: float = field(default=0)
    armor: float = field(default=0)
    ad: float = field(default=0)
    ap: float = field(default=0)
    mr: float = field(default=0)
    movespeed: float = field(default=0)
    movespeedpercent: float = field(default=0)
    attackspeedpercent: float = field(default=0)
    crit: float = field(default=0)
    lifestealpercent: float = field(default=0)
    armorpen: float = field(default=0)
    armorpenpercent: float = field(default=0)
    magicpenpercent: float = field(default=0)
    magicpen: float = field(default=0)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, itemId, item: Dict[str, Any], ):
        itemKeys = {
            "hp": "FlatHPPoolMod",
            "mp": "FlatMPPoolMod",
            "hpregen": "FlatHPRegenMod",
            "armor": "FlatArmorMod",
            "ad": "FlatPhysicalDamageMod",
            "ap": "FlatMagicDamageMod",
            "mr": "FlatSpellBlockMod",
            "ms": "FlatMovementSpeedMod",
            "msPercent": "PercentMovementSpeedMod",
            "attackSpeedPercent": "PercentAttackSpeedMod",
            "crit": "FlatCritChanceMod",
            "lifeStealPercent": "PercentLifeStealMod",
        }
        newDict = dict(id=int(itemId), name=item['name'], tags=item['tags'], armorPenFlat=0, magicPenFlat=0,
                       amorPenPercent=0, magicPenPercent=0, gold=item['gold']['total'])

        for k, v in itemKeys.items():
            if v in item['stats'].keys():
                if k == 'movementspeedpercent':
                    newDict[k] = float(item['stats'][v])
                else:
                    newDict[k] = item['stats'][v]

        for i, tag in enumerate(item['tags']):
            if tag in ("MagicPenetration", "ArmorPenetration"):
                if "effect" in item.keys():
                    effectStr = "Effect{}Amount".format(i + 1)
                    if effectStr in item['effect'].keys():
                        value = float(item['effect'][effectStr])
                        isPercent = value < 1

                        if tag == "MagicPenetration":
                            if isPercent:
                                newDict['magicpenpercent'] = value
                            else:
                                newDict['magicpen'] = value
                        elif tag == "ArmorPenetration":
                            if isPercent:
                                newDict['armorpenpercent'] = value
                            else:
                                newDict['armorpen'] = value
        return from_dict(cls, data=newDict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
