import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataenum.lol.event_type_enum import EventType


@dataclass
class DamageDealt:
    type: str
    basic: bool
    magicDamage: int
    name: str
    participantId: int
    physicalDamage: int
    spellName: str
    spellSlot: int
    trueDamage: int

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "DamageDealt":

        data['type'] = EventType(data['type'])
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
