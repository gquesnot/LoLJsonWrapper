from dataclasses import dataclass, asdict, field
from typing import Any, Union, List, Dict

from dacite import from_dict

from my_dataclass.image import Image
from my_dataclass.lol.spell.spell_lvl import SpellLvl
from my_dataclass.lol.spell.spell_tip import SpellTip
from util.dataclass_function import mapDataClassFields


@dataclass
class Spell:
    id: str
    name: str
    description: str
    tooltip: str
    leveltip: Union[List[SpellTip], None]
    maxrank: int

    # datavalues: Dict[]

    vars: list
    costType: str
    maxammo: int
    spellByLevel: List[SpellLvl]
    image: Image
    resource: Union[str, None] = field(default=None)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Spell":
        # data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        toMap = {
            "leveltip": {
                "list": True,
                "type": SpellTip,
            }
        }
        data['spellByLevel'] = [SpellLvl.from_dict({
            "cooldown": data['cooldown'][i],
            "cost": data['cost'][i],
            "effects": [v[i] if v is not None else None for v in
                        [[v for v in vv] if vv is not None else None for vv in data['effect']]],
            "range": data['range'][i],
            "lvl": i + 1
        }).to_dict() for i in range(data['maxrank'])]
        data['maxammo'] = int(data['maxammo'])
        if "leveltip" in data.keys():

            data['leveltip'] = [{"label": label, "effect": data['leveltip']["effect"][idx]} for idx, label in
                                enumerate(data['leveltip']["label"])]
            data = mapDataClassFields(dc, data, toMap)
        else:
            print("ERROR NO leveltip for the spell", data['name'])

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
