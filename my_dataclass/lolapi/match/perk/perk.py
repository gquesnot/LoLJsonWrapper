import keyword
from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.perk.stats import Stats
from my_dataclass.lolapi.match.perk.style import Style


@dataclass
class Perk:
    stats : Stats# statPerks->defenseId = Stat Value
    styles : List[Style]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Perk":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
