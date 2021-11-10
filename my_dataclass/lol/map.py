from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

@dataclass
class Map:
    id: int
    name: str
    notes : str


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Map":
        #data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        data['id'] = data['mapId']
        data['name'] = data['mapName']
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
