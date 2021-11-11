import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Objective:
    first:bool = field(default=False)
    kills:int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Objective":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
