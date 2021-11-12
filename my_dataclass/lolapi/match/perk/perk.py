from dataclasses import dataclass, asdict
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.perk.participant_runes import ParticipantRunes
from my_dataclass.lolapi.match.perk.stats import Stats


@dataclass
class Perk:
    stats: Stats  # statPerks->defenseId = Stat Value
    runes: ParticipantRunes

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Perk":
        data['stats'] = Stats.from_dict(dc, data['statPerks']).to_dict()
        resRunes = dict()
        data["runes"] = ParticipantRunes.from_dict(dc, data['styles']).to_dict()
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
