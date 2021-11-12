import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.ban import Ban
from my_dataclass.lolapi.match.objectives import Objectives


@dataclass
class Team:
    bans: List[Ban]
    objectives: Objectives
    teamId: int = field(default=0)
    win: bool = field(default=False)
    earlySurrendered: bool = field(default=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
