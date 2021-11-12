import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon


@dataclass
class Rune:

    id: int
    key: str
    icon: str
    name: str
    shortDesc: str
    longDesc: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rune":

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
