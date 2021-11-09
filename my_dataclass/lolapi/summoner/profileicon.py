from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.image import Image


@dataclass
class ProfileIcon:
    id: int
    image: Image


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProfileIcon":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
