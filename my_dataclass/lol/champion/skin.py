
from dataclasses import dataclass, field, asdict
from time import sleep
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

@dataclass
class Skin:
    id: int
    num: int
    name: str
    chromas: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skin":
        data['id'] = int(data['id'])
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



