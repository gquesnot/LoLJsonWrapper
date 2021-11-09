
from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

@dataclass
class Item:
    id: int
    name: str
    description: str
    isunique: bool
    iselusive: bool
    isradiant: bool


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Item":
        data = {k.lower() if k in keyword.kwlist else f"{k.lower()}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)