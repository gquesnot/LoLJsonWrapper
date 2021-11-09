from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

@dataclass
class ItemStats:

    hp: Union[float, None] = field(default=None)
    hpregen: Union[float, None] = field(default=None)
    mp: Union[float, None] = field(default=None)
    mpregen: Union[float, None] = field(default=None)
    movespeed: Union[float, None] = field(default=None)
    movespeedpercent: Union[float, None] = field(default=None)
    armor: Union[float, None] = field(default=None)
    mr: Union[float, None] = field(default=None)
    crit: Union[float, None] = field(default=None)
    ad: Union[float, None] = field(default=None)
    attackspeedpercent: Union[float, None] = field(default=None)
    omnivamppercent: Union[float, None] = field(default=None)
    lifestealpercent: Union[float, None] = field(default=None)
    armorpen: Union[float, None] = field(default=None)
    armorpenpercent: Union[float, None] = field(default=None)
    magicpenpercent: Union[float, None] = field(default=None)
    magicpen: Union[float, None] = field(default=None)
    healshieldpower: Union[float, None] = field(default=None)
    ah: Union[float, None] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ItemStats":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
