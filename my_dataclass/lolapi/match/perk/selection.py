from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lolapi.summoner.rune import Rune


@dataclass
class Selection:
    rune: Rune
    var1: int = field(default=0)
    var2: int = field(default=0)
    var3: int = field(default=0)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Selection":
        # print(data)
        data['rune'] = dc.lol.runes[str(data['perk'])].to_dict()

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
