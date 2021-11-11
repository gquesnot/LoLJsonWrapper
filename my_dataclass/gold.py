import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Gold:

    base: int
    purchasable: int
    total: int
    sell: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Gold":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
