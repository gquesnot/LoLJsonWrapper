from typing import List, Dict, Any

from my_dataclass.wrapper_config import WrapperConfig
from my_dataenum.config_index import ConfigIndex
from util.base_wrapper_function import valToStr


class BaseWrapper:
    dc: Any
    allConfig: List[str]
    hint: str
    configs: List[WrapperConfig]
    configsDict: List[Dict[str, Any]] = []

    def __init__(self, dc):
        from wrapper import LolDataController
        self.dc: LolDataController = dc

        self.allConfig = [config.name for config in self.configs]

    def getConfigByName(self, name):
        for config in self.configs:
            if config.name == name:
                return config
        return None

    def cleanJson(self):
        for config in self.configs:
            if config is not None and config.json is not None:
                config.json = None

    def getClassAsKeyClass(self, config, elem, key=None):
        myClass = config.class_.from_dict(self.dc, elem)

        if myClass is not None:
            if config.configIndex == ConfigIndex.ID:
                key = valToStr(myClass.id)
            elif config.configIndex == ConfigIndex.NAME:
                key = valToStr(myClass.name)
            elif config.configIndex == ConfigIndex.KEY:
                key = valToStr(key)
        else:
            return None, None
        return key, myClass
