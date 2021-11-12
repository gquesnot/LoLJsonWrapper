import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from dacite import from_dict

from my_dataclass.lolapi.match_timeline.frame_participant import FrameParticipant
from my_dataclass.lolapi.summoner.summoner import Summoner


@dataclass
class MatchTimelineParticipant:
    frames: List[FrameParticipant]
    id: int
    summoner: Summoner


    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "MatchTimelineParticipant":
        data['id'] = data['participantId']
        data['summoner'] = Summoner.from_dict(dc, {"puuid":data['puuid']})
        data['frames'] = [FrameParticipant.from_dict(dc, frame)for frame in data['frames']]
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
