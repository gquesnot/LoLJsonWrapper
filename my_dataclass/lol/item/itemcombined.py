from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, Type, Union
from dacite import from_dict
import keyword

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.image import Image
from my_dataclass.lol.item.itemstats import ItemStats
from my_dataclass.gold import Gold



@dataclass
class ItemCombined:
    id: int
    name: str
    description: str
    colloq: str
    plaintext: str

    image: Image
    gold: Gold
    tags: List[str]
    stats: ItemStats
    maps: List[int]
    specialRecipe: Union[int, None] = field(default=None)
    stacks: int = field(default=0)
    depth: int = field(default=0)
    from_:Union[None,List[str]] = field(default=None)
    into: Union[None, List[str]] = field(default=None)
    consumed: bool = field(default=False)
    consumeOnFull: bool = field(default=False)

    requiredChampion: Union[Champion, None] = field(default=None)
    inStore: bool = field(default=True)
    hideFromAll: bool = field(default=False)


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ItemCombined":
        #data = {k if k not in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
