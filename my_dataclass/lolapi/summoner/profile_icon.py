from dataclasses import dataclass, asdict
from typing import Any, Union, Dict

from dacite import from_dict

from my_dataclass.image import Image


@dataclass
class ProfileIcon:
    id: int
    image: Image

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Union["ProfileIcon", None]:
        # data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}

        if isinstance(data['id'], str):
            data['id'] = int(data['id'])

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
