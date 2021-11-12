import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match_timeline.event import Event
from my_dataclass.lolapi.match_timeline.frame_participant import FrameParticipant


@dataclass
class Frame:
    events: List[Event]
    participant: FrameParticipant
    timestamp: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Frame":
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
