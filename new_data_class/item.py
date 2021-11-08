from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from lolClass.data_class.champion import Champion
from new_data_class.image import Image
from new_data_class.stats import Stats
from new_data_class.gold import Gold

def itemParser():
    pass


@dataclass
class Item:

    name: str
    description: str
    colloq: str
    plaintext: str

    image: Image
    gold: Gold
    tags: List[str]
    stats: Stats
    maps: List[int]

    stacks: int = field(default=0)
    depth: int = field(default=0)
    from_: List[str] = field(default=None)
    into: List[str] = field(default=None)
    consumed: bool = field(default=False)
    consumeOnFull: bool = field(default=False)
    specialRecipe: int = field(default=None)
    requiredChampion: Champion = field(default=None)
    inStore: bool = field(default=True)
    hideFromAll: bool = field(default=False)


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Item":
        data = {k if k not in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
