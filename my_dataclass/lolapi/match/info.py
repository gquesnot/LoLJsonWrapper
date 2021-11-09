from dataclasses import dataclass, field, asdict
from typing import Any,  List, Dict
from dacite import from_dict
import keyword

from my_dataclass.lolapi.baseinfo import BaseInfo
from my_dataclass.lolapi.match.team import Team


@dataclass
class Info(BaseInfo):
    gameMode: GameModeType # gameMode + gameType + mapId => GameModeType
    teams: List[Team] = field(default=[])
    gameCreation: int = field(default=0)
    gameDuration: int = field(default=0)
    gameEndTimestamp: int = field(default=0)
    gameId: int = field(default=0)

    gameName: str = field(default=None)
    gameStartTimestamp: int = field(default=None)
    gameType: str = field(default=None)
    gameVersion: str = field(default=None)
    mapId: int = field(default=None)
    platformId: str = field(default=None)
    queueId: int = field(default=None)
    tournamentCode: str = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Info":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
