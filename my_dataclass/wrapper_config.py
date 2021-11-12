from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict

import util
from my_dataenum.config_index import ConfigIndex


@dataclass
class WrapperConfig:
    name: str
    id: int
    class_: Any
    datas: Dict[str, Any] = field(default_factory=dict)
    json: Union[List, Dict] = field(default=None)

    def addData(self, key, newClass):
        if newClass is not None:
            if isinstance(newClass, self.class_):
                self.datas[key] = newClass

    @classmethod
    def from_dict(cls, idx: int, data: Dict[str, Any]) -> "WrapperConfig":
        data['id'] = idx
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
