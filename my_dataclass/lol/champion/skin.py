
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class Skin:
    id: int
    num: int
    name: str
    chromas: bool

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Skin":
        data['id'] = int(data['id'])
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



