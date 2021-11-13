from dataclasses import dataclass
from typing import Any, Dict

from dacite import from_dict

from util.wrapper_config import WrapperConfig
from util.base_wrapper_function import withoutDataDict


@dataclass
class ApiWrapperConfig(WrapperConfig):

    def setJson(self, datas):
        self.json = withoutDataDict(datas)

    @classmethod
    def from_dict(cls, idx: int, data: Dict[str, Any]) -> "ApiWrapperConfig":
        data['id'] = idx
        return from_dict(cls, data=data)
