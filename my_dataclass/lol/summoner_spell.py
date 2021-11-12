
from dataclasses import dataclass, asdict, field
from typing import Any, Union, List, Dict

from dacite import from_dict

from my_dataclass.image import Image
from my_dataclass.lol.spell.spell_lvl import SpellLvl


@dataclass
class SummonerSpell:
    id: int
    name: str
    description: str
    tooltip: str
    datavalues: dict
    spellByLevel: SpellLvl
    #effectBurn: List[Union[None, int]]
    vars : list
    summonerLevel: int
    modes:List[str]
    costType:str
    maxammo: int
    image: Image
    ressource: Union[None, str]
    casts:  int = field(default=0)

    @classmethod
    def from_dict(cls,dc, data: Dict[str, Any]) -> Union["SummonerSpell", None]:
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        if "key" not in data:
            return None
        data['id'] = int(data['key'])
        data['maxammo'] = int(data['maxammo'])
        data['spellByLevel'] = {
            "cooldown": data['cooldown'][0],
            "cost": data['cost'][0],
            "range": data['range'][0],
            "effects":[v[0] if v is not None else None for v in
                        [[v for v in vv] if vv is not None else None for vv in data['effect']]],
            "lvl": 1,

        }
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)