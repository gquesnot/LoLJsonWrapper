from dataclasses import dataclass, asdict
from typing import Any, List, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.perk.selection import Selection
from my_dataclass.lolapi.summoner.rune_path import RunePath


@dataclass
class Style:
    path: RunePath  # statPerks->defenseId = Stat Value
    selections: List[Selection]

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Style":
        resSelections = []
        for selection in data['selections']:
            resSelections.append(Selection.from_dict(dc, selection).to_dict())
        data['selections'] = resSelections
        try:
            data['path'] = dc.lol.runes[str(data['style'])].to_dict()
        except:
            data['path'] = dc.lol.runesPath[str(data['style'])].to_dict()

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
