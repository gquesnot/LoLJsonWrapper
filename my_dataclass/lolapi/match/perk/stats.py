from dataclasses import dataclass, asdict
from typing import Any, Dict
from dacite import from_dict
import keyword

from my_dataclass.lolapi.match.perk.stat import Stat


@dataclass
class Stats:
    defense: Stat
    flex: Stat
    offense: Stat

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stats":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
