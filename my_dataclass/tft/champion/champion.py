
from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.tft.trait.trait import Trait


@dataclass
class Champion:
    name:str
    id: str
    cost: int
    traits: List[Trait]


    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Champion":
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        data['id'] = data['championId']
        data['traits'] = myTraits = [dc.tft.traits[trait] for trait in data['traits']]
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)