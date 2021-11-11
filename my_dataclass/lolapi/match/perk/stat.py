import keyword
from dataclasses import dataclass, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict


@dataclass
class Stat:
    id: int
    type: str
    value: Union[int, List[int]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stat":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
