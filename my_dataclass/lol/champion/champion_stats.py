from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class ChampionStats:
    hp: float = field(default=0)
    mp: float = field(default=0)
    moveSpeed: float = field(default=0)
    armor: float = field(default=0)
    armorPerLevel: float = field(default=0)
    mr: float = field(default=0)
    mrPerLevel: float = field(default=0)
    cdr: float = field(default=0)
    hpRegen: float = field(default=0)
    mpRegen: float = field(default=0)
    crit: float = field(default=0)
    ad: float = field(default=0)
    ah: float = field(default=0)
    attackRange: float = field(default=0)
    attackSpeed: float = field(default=0)
    hpMax: float = field(default=0)
    mpMax: float = field(default=0)
    hpPerLevel: float = field(default=0)
    mpPerLevel: float = field(default=0)
    hpRegenperLevel: float = field(default=0)
    mpRegenperLevel: float = field(default=0)
    critPerLevel: float = field(default=0)
    adPerLevel: float = field(default=0)
    attackSpeedPerlevel: float = field(default=0)
    ap: float = field(default=0)
    ccReductionPercent: float = field(default=0)
    omnivampPercent: float = field(default=0)
    physicalampPercent: float = field(default=0)
    lifestealPercent: float = field(default=0)
    armorPen: float = field(default=0)
    armorPenPercent: float = field(default=0)
    magicPenPercent: float = field(default=0)
    magicPen: float = field(default=0)
    healShieldPower: float = field(default=0)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "ChampionStats":
        data['hpPerLevel'] = data['hpperlevel']
        data['mpPerLevel'] = data['mpperlevel']
        data['moveSpeed'] = data['movespeed']
        data['armorPerLevel'] = data['armorperlevel']
        data['mr'] = data['spellblock']
        data['mrPerLevel'] = data['spellblockperlevel']
        data['attackRange'] = data['attackrange']
        data[''] = data['hpregen']
        data['hpRegenPerLevel'] = data['hpregenperlevel']
        data['mpRegen'] = data['mpregen']
        data['mpRegenPerLevel'] = data['mpregenperlevel']
        data['critPerLevel'] = data['critperlevel']
        data['ad'] = data['attackdamage']
        data['adPerLevel'] = data['attackdamageperlevel']
        data['attackSpeedPerLevel'] = data['attackspeedperlevel']
        data['attackSpeed'] = data['attackspeed']

        return from_dict(cls, data=data)

    @classmethod
    def from_dictMatchTimeline(cls, data: Dict[str, Any]):
        data['ah'] = data['abilityHaste']
        data['ap'] = data['abilityPower']
        data['ad'] = data['attackDamage']
        data['ccReductionPercent'] = data['ccReduction']
        data['cdr'] = data['cooldownReduction']
        data['hp'] = data['health']
        data['hpMax'] = data['healthMax']
        data['hpRegen'] = data['healthRegen']
        data['lifestealPercent'] = data['lifesteal']
        data['mr'] = data['magicResist']
        data['omnivampPercent'] = data['omnivamp']
        data['physicalVampPercent'] = data['physicalVamp']
        data['mp'] = data['power']
        data['mpMax'] = data['powerMax']
        data['mpRegen'] = data['powerRegen']
        data['spellVampPercent'] = data['spellVamp']
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


