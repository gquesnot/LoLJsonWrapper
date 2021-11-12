from dataclasses import dataclass, field, asdict
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.ban import Ban
from my_dataclass.lolapi.match.objective import Objective


@dataclass
class TeamInfo:
    id: int
    win: bool
    bans: List[Ban]
    objectives: Dict[str, Objective] = field(
        default_factory={"baron": None, "champion": None, "dragon": None, "inhibitor": None, "riftHerald": None,
                         "tower": None})
    earlySurrender: bool = field(default=False)
    surrender: bool = field(default=False)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any], idx: int) -> "TeamInfo":
        data['id'] = idx
        data['bans'] = [Ban.from_dict(dc, ban).to_dict() for ban in data['bans']]
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
