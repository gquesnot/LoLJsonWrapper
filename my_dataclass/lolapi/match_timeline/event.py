import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Union, List

from dacite import from_dict

from my_dataclass.lolapi.match_timeline.damage_dealt import DamageDealt
from my_dataclass.position import Position
from my_dataenum.lol.event_type_enum import EventType


@dataclass
class Event:
    realTimestamp: Union[int, None] = field(default=None)
    timestamp: Union[int, None] = field(default=None)
    type: EventType = field(default=None)
    participantId: Union[int, None] = field(default=None)
    creatorId: Union[int, None] = field(default=None)
    victimId: Union[int, None] = field(default=None)
    killerId: Union[int, None] = field(default=None)
    skillSlot: Union[int, None] = field(default=None)
    levelUpType: Union[str, None] = field(default="")
    level: Union[int, None] = field(default=None)
    itemId: Union[int, None] = field(default=None)

    assistingParticipantIds: Union[List[int], None] = field(default=None)
    bounty: Union[int, None] = field(default=None)
    killStreakLength: Union[int, None] = field(default=None)
    position: Union[Position, None] = field(default=None)
    victimDamageDealt: Union[List[DamageDealt], None] = field(default=None)
    victimDamageReceived: Union[List[DamageDealt], None] = field(default=None)
    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Event":
        type_ = EventType(data['type'])
        if type_ == EventType.CHAMPION_KILL:
            if "victimDamageDealt" in data.keys():
                data['victimDamageDealt'] = [DamageDealt.from_dict(dc, v).to_dict() for v in data['victimDamageDealt']]
            if "victimDamageReceived" in data.keys():
                data['victimDamageReceived'] = [DamageDealt.from_dict(dc, v).to_dict() for v in
                                            data['victimDamageReceived']]
        data['type'] = type_


        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
