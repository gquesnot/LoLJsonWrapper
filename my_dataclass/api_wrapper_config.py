from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict

import util
from my_dataclass.wrapper_config import WrapperConfig
from my_dataenum.config_index import ConfigIndex
from util.base_wrapper_function import withoutDataDict


@dataclass
class ApiWrapperConfig(WrapperConfig):

    def setJson(self, datas):
        self.json = withoutDataDict(datas)

    @classmethod
    def from_dict(cls, idx: int, data: Dict[str, Any]) -> "ApiWrapperConfig":
        data['id'] = idx
        return from_dict(cls, data=data)
