import copy
from dataclasses import dataclass, field

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
    name: str
    id: int
    hp: float
    hpperlevel: float
    mp: float
    mpperlevel: float
    movespeed: float
    armor: float
    armorperlevel: float
    mr: float
    mrperlevel: float
    attackrange: float
    hpregen: float
    hpregenperlevel: float
    mpregen: float
    mpregenperlevel: float
    crit: float
    critperlevel: float
    ad: float
    adperlevel: float
    attackspeedperlevel: float
    attackspeed: float

    lvl: int = field(default=0)

    armorpen: float = field(init=False, default=0)
    armorpenpercent: float = field(init=False, default=0)
    magicpen: float = field(init=False, default=0)
    magicpenpercent: float = field(init=False, default=0)
    abilityhaste: int = field(init=False, default=0)
    ap: float = field(init=False, default=0)
    lifesteal: float = field(init=False, default=0)
    omnivamp: float = field(init=False, default=0)
    physicalvamp: float = field(init=False, default=0)

    def byLevel(self, lvl):
        lvl = lvl - 1
        self.hp += self.hpperlevel * lvl
        self.mp += self.mpperlevel * lvl
        self.armor += self.armorperlevel * lvl
        self.mr += self.mrperlevel * lvl
        self.attackspeed = self.attackspeed * (1 + (self.attackspeedperlevel / 100 * lvl))
        self.ad += self.adperlevel * lvl
        self.lvl = lvl



    def updateWithFrame(self, frameData):
        self.armor = frameData['armor']
        self.abilityhaste = frameData['abilityHaste']
        self.ap = frameData['abilityPower']
        self.armorpen = frameData['armorPen']
        self.armorpenpercent = frameData['armorPenPercent'] / 100
        self.ad = frameData['attackDamage']
        self.attackspeed = frameData['attackSpeed'] / 100
        self.hp = frameData['healthMax']
        self.mp = frameData['powerMax']
        self.omnivamp = frameData['omnivamp']
        self.physicalvamp = frameData['physicalVamp']
        self.lifesteal = frameData['lifesteal']

        self.magicpen = frameData['magicPen']
        self.magicpenpercent = frameData['magicPenPercent'] / 100
        self.movespeed = frameData['movementSpeed']

    def addItemStat(self, item):
        for k ,v in itemStatList.items():
            myValue = getattr(self, k)
            itemValue = getattr(item, v)
            resValue = myValue + itemValue
            setattr(self, k, resValue)
