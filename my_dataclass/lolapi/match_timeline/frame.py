import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match_timeline.event import Event
from my_dataclass.lolapi.match_timeline.participant_frame import ParticipantFrame


@dataclass
class Frame:
    events: List[Event]
    participantFrames: List[str, ParticipantFrame]
    timestamp: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Frame":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
