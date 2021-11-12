
from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.tft.trait.set import Set
from my_dataenum.tft.trait_types import TraitType


@dataclass
class Trait:
    id: str
    name: str
    description: str
    type: TraitType
    sets: List[Set]


    @classmethod
    def from_dict(cls, dc,data: Dict[str, Any]) -> "Trait":
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        data['id'] = data['key']
        data["type"] = TraitType(data['type'])
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)