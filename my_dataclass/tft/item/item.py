
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Item:
    id: int
    name: str
    description: str
    isUnique: bool
    isElusive: bool
    isRadiant: bool


    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Item":
        #data = {k.lower() if k in keyword.kwlist else f"{k.lower()}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)