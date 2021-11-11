from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class GameMode:

    name :str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameMode":
        data['name'] = data['gameMode']
        #data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
