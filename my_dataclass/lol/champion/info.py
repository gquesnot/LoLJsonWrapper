from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Info:
    attack: int
    defense: int
    magic: int
    difficulty: int

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Info":
        # data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
