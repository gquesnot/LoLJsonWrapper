import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.position import Position


@dataclass
class Coor(Position):
    w: int = field(default=0)
    h: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Coor":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
