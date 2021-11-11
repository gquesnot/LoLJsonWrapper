import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Selection:
    perk: int = field(default=0)
    var1: int = field(default=0)
    var2: int = field(default=0)
    var3: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Selection":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
