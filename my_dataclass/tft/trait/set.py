
from dataclasses import dataclass, field, asdict
from typing import Any, Union, Dict

from dacite import from_dict


@dataclass
class Set:
    style: str
    min: int
    max: Union[int, None] = field(default=None)


    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Set":
        #data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        # data["min"] = int(data["min"])
        # if "max" in data.keys():
        #     data["max"]= int(data["max"])
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)