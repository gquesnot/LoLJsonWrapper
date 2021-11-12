from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.perk.style import Style


@dataclass
class ParticipantRunes:
    primary: Style
    secondary: Style

    @classmethod
    def from_dict(cls, dc, data: List[Any]) -> "ParticipantRunes":
        res = dict()
        for rune in data:
            if rune['description'] == "primaryStyle":

                res['primary'] = Style.from_dict(dc, rune).to_dict()
            elif rune['description'] == "subStyle":
                res['secondary'] = Style.from_dict(dc, rune).to_dict()

        return from_dict(cls, data=res)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
