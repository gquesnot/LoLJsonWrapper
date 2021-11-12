import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from dacite import from_dict

from my_dataclass.lolapi.game_info import GameInfo
from my_dataclass.lolapi.match_timeline.frame_participant import FrameParticipant
from my_dataclass.lolapi.match_timeline.participant import MatchTimelineParticipant


@dataclass
class MatchTimeline:
    id: str
    gameId: int
    frameInterval: int
    participants: List[MatchTimelineParticipant]

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "MatchTimeline":
        data['id'] = data['metadata']['matchId']
        data['gameId'] = data['info']['gameId']
        data['frameInterval'] = data['info']['frameInterval']
        participants = data['info']['participants']
        for participant in participants:
            pId = participant['participantId']
            pIdStr = str(pId)
            resFrames = []
            for frame in data['info']['frames']:
                tmpFrame = frame['participantFrames'][pIdStr]
                tmpFrame["events"] = []

                for event in frame['events']:
                    for k in ["participantId", "creatorId", "killerId", "victimId"]:
                        if k in event.keys() and pId == event[k]:
                            tmpFrame['events'].append(event)
                resFrames.append(tmpFrame)
            participants[pId - 1]['frames'] = resFrames

        data['participants'] = [MatchTimelineParticipant.from_dict(dc, participant).to_dict() for participant in participants]
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
