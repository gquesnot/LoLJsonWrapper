from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Image:

    full: str
    sprite: str
    group: str
    x: int
    y: int
    w: int
    h: int

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Image":
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
