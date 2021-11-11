import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lolapi.match_timeline.info import Info
from my_dataclass.lolapi.metadata import Metadata


@dataclass
class Matchtimeline:
    metadata: Metadata
    info: Info

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Matchtimeline":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
