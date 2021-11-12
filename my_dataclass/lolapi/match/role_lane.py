from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class RoleLane:
    role: str
    lane: str
    teamPosition: str
    individualPosition: str

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "RoleLane":
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
