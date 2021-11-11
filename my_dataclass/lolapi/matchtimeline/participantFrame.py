from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.lol.champion.champion_stats import ChampionStats
from my_dataclass.lolapi.matchtimeline.damage_stat import DamageStat
from my_dataclass.position import Position


@dataclass
class ParticipantFrame:
    championStats: ChampionStats
    damageStats: DamageStat
    position: Position
    currentGold: int = field(default=0)
    goldPerSecond: int = field(default=0)
    jungleMinionsKilled: int = field(default=0)
    level: int = field(default=0)
    minionsKilled: int = field(default=0)
    participantId: int = field(default=0)
    timeEnemySpentControlled: int = field(default=0)
    totalGold: int = field(default=0)
    xp: int = field(default=0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParticipantFrame":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
