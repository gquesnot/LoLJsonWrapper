import keyword
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from my_dataclass.lol.champion.champion_stats import ChampionStats
from my_dataclass.image import Image
from my_dataclass.lol.champion.info import Info
from my_dataclass.lol.champion.skin import Skin
from my_dataclass.lol.spell.spell import Spell
from util.dataclass_function import mapDataClassFields

itemStatList = {
    "hp": "hp",
    "hpregen": "hpregen",
    "armor": "armor",
    "ad": "ad",
    "ap": "ap",
    "mr": "mr",
    "movespeed": "movespeed",
    "attackspeed": "attackspeedpercent",
    "crit": "crit",
    "lifesteal": "lifestealpercent",
    "armorpen": "armorpen",
    "armorpenpercent": "armorpenpercent",
    "magicpenpercent": "magicpenpercent",
    "magicpen": "magicpen",
}


@dataclass
class Champion:
    id: int
    name: str
    title: str
    blurb: str
    info: Info
    image: Image
    tags: List[str]
    partype: str
    stats: ChampionStats
    enemytips: List[str]
    allytips: List[str]
    lore: str
    skins: List[Skin]
    spells: List[Spell]
    lvl: int = field(default=0)

    @classmethod
    def from_dict(cls, dataFull: Dict[str, Any], dataLight: Dict[str, Any]) -> "Champion":
        champName = dataLight['name']
        dataFull = list(dataFull.values())[0]
        data = dataFull

        toMap = {
            "stats": {
                "list": False,
                "type": ChampionStats,
            },
            "skins": {
                "list": True,
                "type": Skin
            },
            "spells": {
                "list": True,
                "type": Spell
            },
            "info": {
                "list": False,
                "type": Info
            },
            "image": {
                "list": False,
                "type": Image
            }
        }
        data['id'] = int(dataLight['key'])
        data= mapDataClassFields(data, toMap)

        #data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        return from_dict(cls, data=data)



    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def byLevel(self, lvl):
        self.lvl = lvl
        lvl = lvl - 1
        self.stats.hp += self.stats.hpperlevel * lvl
        self.stats.mp += self.stats.mpperlevel * lvl
        self.stats.armor += self.stats.armorperlevel * lvl
        self.stats.mr += self.stats.mrperlevel * lvl
        self.stats.attackspeed = self.stats.attackspeed * (1 + (self.stats.attackspeedperlevel / 100 * lvl))
        self.stats.ad += self.stats.adperlevel * lvl

    def updateWithFrame(self, frameData):
        self.stats.armor = frameData['armor']
        self.stats.ah = frameData['abilityHaste']
        self.stats.ap = frameData['abilityPower']
        self.stats.armorpen = frameData['armorPen']
        self.stats.armorpenpercent = frameData['armorPenPercent'] / 100
        self.stats.ad = frameData['attackDamage']
        self.stats.attackspeed = frameData['attackSpeed'] / 100
        self.stats.hp = frameData['healthMax']
        self.stats.mp = frameData['powerMax']
        self.stats.omnivamppercent = frameData['omnivamp']
        self.stats.physicalvamppercent = frameData['physicalVamp']
        self.stats.lifestealpercent = frameData['lifesteal']

        self.stats.magicpen = frameData['magicPen']
        self.stats.magicpenpercent = frameData['magicPenPercent'] / 100
        self.stats.movespeed = frameData['movementSpeed']

    def addItemStat(self, item):
        for k, v in itemStatList.items():
            myValue = getattr(self, k)
            itemValue = getattr(item, v)
            resValue = myValue + itemValue
            setattr(self, k, resValue)
