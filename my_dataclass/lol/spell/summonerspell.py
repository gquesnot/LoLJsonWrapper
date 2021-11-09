
from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.image import Image


@dataclass
class SummonerSpell:
    id: int
    name: str
    description: str
    tooltip: str
    cooldown: int
    datavalues: dict
    effect: List[Union[None, List[int]]]
    effectBurn: List[Union[None, int]]
    vars_: list
    summonerlevel: int
    modes:List[str]
    costType:str
    maxammo: int
    range: int
    image: Image
    ressource: Union[None, str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SummonerSpell":
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)