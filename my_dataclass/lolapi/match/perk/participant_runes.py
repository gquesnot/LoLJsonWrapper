import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.perk.selection import Selection
from my_dataclass.lolapi.match.perk.style import Style
from my_dataenum.lol.perk_enum import PerkEnum


@dataclass
class ParticipantRunes:
    primary: Style
    secondary : Style

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
