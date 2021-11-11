from dataclasses import dataclass, field, asdict
from typing import Any,  List, Dict
from dacite import from_dict
import keyword

from my_dataclass.lolapi.base_info import BaseInfo
from my_dataclass.lolapi.match_timeline.frame import Frame


@dataclass
class Info(BaseInfo):
    frames: List[Frame] = field(default=[])
    frameInterval: int = field(default=None)
    gameId: int = field(default=None)


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Info":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
