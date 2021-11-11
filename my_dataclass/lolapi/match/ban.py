import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lol.champion.champion import Champion


@dataclass
class Ban:
    champion: Champion#championId -> Champion
    pickTurn: int = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ban":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
