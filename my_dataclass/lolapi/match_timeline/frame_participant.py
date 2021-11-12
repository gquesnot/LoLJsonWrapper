import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from dacite import from_dict

from my_dataclass.lol.champion.champion_stats import ChampionStats
from my_dataclass.lolapi.match_timeline.damage_stat import DamageStat
from my_dataclass.lolapi.match_timeline.event import Event
from my_dataclass.lolapi.summoner.summoner import Summoner
from my_dataclass.position import Position


@dataclass
class FrameParticipant:
    championStats: ChampionStats
    damageStats: DamageStat
    position: Position
    events : List[Event]
    gold : int = field(default=0)
    goldPerSecond: int = field(default=0)
    jungleMinionsKilled: int = field(default=0)
    level: int = field(default=0)
    minionsKilled: int = field(default=0)
    id: int = field(default=0)
    timeEnemySpentControlled: int = field(default=0)
    totalGold: int = field(default=0)
    xp: int = field(default=0)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "FrameParticipant":
        data['gold'] = data['currentGold']
        data['championStats'] = ChampionStats.from_dictMatchTimeline(data['championStats'])
        data['events'] = [Event.from_dict(dc, event).to_dict() for event in data['events']]
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
