import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class DamageStat:
    magicDamageDone: int = field(default=0)
    magicDamageDoneToChampions: int = field(default=0)
    magicDamageTaken: int = field(default=0)
    physicalDamageDone: int = field(default=0)
    physicalDamageDoneToChampions: int = field(default=0)
    physicalDamageTaken: int = field(default=0)
    totalDamageDone: int = field(default=0)
    totalDamageDoneToChampions: int = field(default=0)
    totalDamageTaken: int = field(default=0)
    trueDamageDone: int = field(default=0)
    trueDamageDoneToChampions: int = field(default=0)
    trueDamageTaken: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DamageStat":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
