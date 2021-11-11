import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict

from my_dataclass.lolapi.match.objective import Objective


@dataclass
class Objectives:
    baron: Objective
    champion: Objective
    dragon: Objective
    inhibitor: Objective
    riftHerald: Objective
    tower: Objective

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Objectives":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
