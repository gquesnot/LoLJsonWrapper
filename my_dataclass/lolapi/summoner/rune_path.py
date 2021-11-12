import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from dacite import from_dict

from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon
from my_dataclass.lolapi.summoner.rune import Rune


@dataclass
class RunePath:

    id: int
    key: str
    name: str
    icon: str
    runes: List[List[Rune]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], runesDict) -> "RunePath":
        data['runes'] = runesDict
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
