import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict

from my_dataclass.lol.game_mode import GameMode
from my_dataclass.lol.game_type import GameType
from my_dataclass.lol.map import Map
from my_dataclass.lol.queue import Queue
from my_dataclass.lolapi.match.team_info import TeamInfo


@dataclass
class GameInfo:
    creationTimestamp: int
    duration: int
    id: int
    mode: GameMode
    type: GameType
    name: str
    version : str
    startTimestamp: int
    map: Map
    queue: Queue
    platformId: str
    team1 : TeamInfo
    team2 : TeamInfo
    tournamentCode: str= field(default="")


    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "GameInfo":
        # data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        data['mode'] = dc.lol.gameModes[data['gameMode']].to_dict()
        data['map'] = dc.lol.maps[str(data['mapId'])].to_dict()
        data['type'] = dc.lol.gameTypes[data['gameType']].to_dict()
        data['queue'] = dc.lol.queues[str(data['queueId'])].to_dict()
        data['creationTimestamp'] = data['gameCreation']
        data['duration'] = data['gameDuration']
        data['endTimestamp'] = data['gameEndTimestamp']
        data['startTimestamp'] = data['gameStartTimestamp']
        data['version'] = data['gameVersion']
        data['name'] = data['gameName']
        data['id'] = data['gameId']
        data['team1'] = TeamInfo.from_dict(dc, data['teams'][0], 1).to_dict()
        data['team2'] = TeamInfo.from_dict(dc, data['teams'][1], 2).to_dict()


        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
