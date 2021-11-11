import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict


@dataclass
class Metadata:
    participants: List[str]
    dataVersion: str = field(default=None)
    matchId: str = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Metadata":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
