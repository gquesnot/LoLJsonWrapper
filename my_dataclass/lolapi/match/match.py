import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.game_info import GameInfo
from my_dataclass.lolapi.match.match_participant import MatchParticipant

from util.dataclass_function import mapDataClassFields


@dataclass
class Match:
    id: str
    dataVersion : str
    gameInfo: GameInfo
    participants: List[MatchParticipant]= field(default_factory=list)


    @classmethod
    def from_dict(cls, dc,data: Dict[str, Any]) -> "Match":

        gameInfo = GameInfo.from_dict(dc, data['info'])

        data['id'] = data['metadata']['matchId']
        data['dataVersion'] = data['metadata']['dataVersion']
        resParticipant = []
        for idx, participant in enumerate(data['info']['participants']):
            team = gameInfo.team1 if participant['teamId'] == gameInfo.team1.id else gameInfo.team2
            if participant['teamEarlySurrendered'] != team.earlySurrender:
                team.earlySurrender = not team.earlySurrender
            if not team.win:
                if participant['gameEndedInSurrender']:
                    team.surrender = True
            resParticipant.append(MatchParticipant.from_dict(dc, participant, idx, team).to_dict())
        data['participants'] = resParticipant
        data['gameInfo'] = gameInfo.to_dict()
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
