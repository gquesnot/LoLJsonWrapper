from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict



@dataclass
class Event:

    realTimestamp: int = field(default=-1)
    timestamp: int = field(default=-1)
    type: str = field(default=None)
    participantId: int = field(default=-1)
    creatorId: int = field(default=-1)
    skillSlot: int = field(default=-1)
    levelUpType: str = field(default="")
    level: int = field(default=-1)
    itemId: int = field(default=-1)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
