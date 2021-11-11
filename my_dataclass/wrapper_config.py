from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict

from dacite import from_dict

import util
from my_dataenum.config_index import ConfigIndex


@dataclass
class WrapperConfig:
    name: str
    id:int
    path: Union[str, List[str], None]
    configIndex: Union[ConfigIndex, None]
    class_: Any
    url: Union[str, List[str]] = field(default=None)
    inDataDict: bool = field(default=True)
    urlHint: str = field(default="")
    datas: Dict[str, Any] = field(default_factory=dict)
    json: Union[List, Dict] = field(default=None)

    def setJson(self, datas):
        datas = util.withoutDataDict(datas)
        if self.url is not None and (isinstance(self.url, list) and len(self.url) > 1):
            if self.json is None:
                self.json = []
            self.json.append(datas)
        else:
            self.json = datas

    def addData(self, key,newClass):
        if newClass is not None:
            if isinstance(newClass, self.class_):
                self.datas[key] = newClass

    @classmethod
    def from_dict(cls,idx:int, data: Dict[str, Any]) -> "WrapperConfig":
        data['id'] = idx
        if "path" not in data.keys():
            data['path'] = data['name']
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
