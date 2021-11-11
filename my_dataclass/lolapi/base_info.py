from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.lolapi.match.participant import MatchParticipant
from my_dataclass.lolapi.match_timeline.participant import MatchTimeLineParticipant


@dataclass
class BaseInfo:
    participants: List[Union[MatchParticipant, MatchTimeLineParticipant]]= field(default=[])



    gameId: int = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Info":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
