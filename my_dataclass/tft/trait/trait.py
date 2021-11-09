
from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.tft.trait.set import Set
from my_dataenum.tft.traittype import TraitType


@dataclass
class Trait:
    id: str
    name: str
    description: str
    type: TraitType
    sets: List[Set]


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trait":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)