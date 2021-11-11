from __future__ import annotations
import json
import os.path
from typing import Dict, Any, List

from my_dataclass.wrapper_config import WrapperConfig
from my_dataenum.config_index import ConfigIndex
from util.dataclass_function import ownCapitalize
from util.jsonfunction import saveJsonApiResponseInJsonFile
from wrapper.base_wrapper_function import getClassAsKeyClass


class BaseWrapper:
    dc: "LolDataController"
    configs: List[WrapperConfig]
    configsDict: List[Dict[Any]]
    allConfig: List[str]
    hint: str
    basePath: str

    def __init__(self, dc):
        self.dc = dc
        self.basePath = os.path.join(self.dc.basePath, self.hint)
        self.configs = [WrapperConfig.from_dict(idx, config) for idx, config in enumerate(self.configsDict)]
        self.allConfig = [config.name for config in self.configs]

    def load(self, configsList=None, clean=True):
        if configsList is not None:
            hasError = len([1 for config in configsList if config not in self.allConfig]) != 0
            if hasError:
                print("HAS ERROR IN CONFIG")
                return
        else:
            configsList = self.allConfig
        print(f"init {self.hint} datas ...", end="")
        # init function
        self.initConfigs()
        print(f" done")
        for idx, config in enumerate(self.configs):
            configName = config.name
            if configName in configsList:
                configC = ownCapitalize(configName)
                print(f"loading {self.hint} {configName} ... ", end="")
                try:
                    self.configs[idx] = getattr(self, f"load{configC}")()
                except:
                    self.configs[idx] = self.loadConfig(config)
                config = self.configs[idx]
                setattr(self, config.name, config.datas)
                print(f"done")
        if clean:
            self.cleanJson()

    def cleanJson(self):
        for config in self.configs:
            if config.json is not None:
                config.json = None

    def initConfigs(self):
        for idx, config in enumerate(self.configs):
            try:
                self.configs[idx] = getattr(self, f"init{ownCapitalize(config.name)}")()
            except:
                self.configs[idx] = self.initConfig(config)

    def initConfig(self, config):
        path = os.path.join(self.basePath, f"{config.path}.json")

        if self.dc.downloadNewVersion:
            print(f"updating {config.name} ... ", end="")
            url = config.url.format(self.dc.version) if "version" in config.urlHint.split(" ") else config.url
            jsonData = saveJsonApiResponseInJsonFile(url, path)
            print("done")
        else:
            with open(path, "r") as f:
                jsonData = json.load(f)
        config.setJson(jsonData)
        return config

    @staticmethod
    def loadConfig(config):
        jsonDatas = config.json
        res = dict()
        if isinstance(jsonDatas, list):
            for elem in jsonDatas:
                k, v = getClassAsKeyClass(config, elem)
                config.addData(k, v)
        elif isinstance(jsonDatas, dict):
            for key, val in jsonDatas.items():
                k, v = getClassAsKeyClass(config, val, key)
                config.addData(k, v)
        return config

    def getConfigByName(self, name):
        for config in self.configs:
            if config.name == name:
                return config
        return None

    def getDatas(self, configName):
        if configName in self.allConfig:
            return getattr(self, configName)
        return None

    def getPath(self, path):

        return os.path.join(self.basePath, path) if isinstance(path, str) else os.path.join(self.basePath, *path)
