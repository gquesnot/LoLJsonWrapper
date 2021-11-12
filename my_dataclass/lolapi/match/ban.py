import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lol.champion.champion import Champion


@dataclass
class Ban:
    champion: Champion  # championId -> Champion
    pickTurn: int = field(default=None)

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any], ) -> "Ban":
        data['champion'] = dc.lol.getChampById(data['championId']).to_dict()
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
