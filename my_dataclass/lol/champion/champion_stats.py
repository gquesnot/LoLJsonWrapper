import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class ChampionStats:
    hp: float = field(default=0)
    mp: float = field(default=0)
    movespeed: float = field(default=0)
    armor: float = field(default=0)
    armorperlevel: float = field(default=0)
    mr: float = field(default=0)
    mrperlevel: float = field(default=0)
    hpregen: float = field(default=0)
    mpregen: float = field(default=0)
    crit: float = field(default=0)
    ad: float = field(default=0)
    ah: float = field(default=0)
    attackrange: float = field(default=0)
    attackspeed: float = field(default=0)
    hpmax: float = field(default=0)
    mpmax: float = field(default=0)
    hpperlevel: float = field(default=0)
    mpperlevel: float = field(default=0)
    hpregenperlevel: float = field(default=0)
    mpregenperlevel: float = field(default=0)
    critperlevel: float = field(default=0)
    adperlevel: float = field(default=0)
    attackspeedperlevel: float = field(default=0)
    ap : float = field(default=0)
    ccreductionpercent: float= field(default=0)
    omnivamppercent: float = field(default=0)
    physicalvamppercent: float = field(default=0)
    lifestealpercent: float = field(default=0)
    armorpen: float = field(default=0)
    armorpenpercent: float = field(default=0)
    magicpenpercent: float = field(default=0)
    magicpen: float = field(default=0)
    healshieldpower: float = field(default=0)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "ChampionStats":
        data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
