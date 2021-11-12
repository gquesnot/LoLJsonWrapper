from __future__ import annotations

import json
import os.path
from typing import Dict, Any, List

from my_dataclass.json_wrapper_config import JsonWrapperConfig
from util.base_wrapper import BaseWrapper
from util.json_function import saveJsonApiResponseInJsonFile


class BaseJsonWrapper(BaseWrapper):
    configs: List[JsonWrapperConfig]
    basePath: str

    def __init__(self, dc):
        self.configs = [JsonWrapperConfig.from_dict(idx, config) for idx, config in enumerate(self.configsDict)]
        super().__init__(dc)
        self.basePath = os.path.join(self.dc.basePath, self.hint)

    def load(self, configsList=None, clean=True):
        if configsList is not None:
            hasError = len([1 for config in configsList if config not in self.allConfig]) != 0
            if hasError:
                if self.dc.showLog:
                    print("HAS ERROR IN CONFIG")
                return
        else:
            configsList = self.allConfig
        if self.dc.showLog:
            print(f"init {self.hint} datas ...", end="")
        # init function
        self.initConfigs()
        if self.dc.showLog:
            print(f" done")
        for idx, config in enumerate(self.configs):
            configName = config.name
            if configName in configsList:
                configC = self.dc.ownCapitalize(configName)
                if self.dc.showLog:
                    print(f"loading {self.hint} {configName} ... ", end="")
                try:
                    self.configs[idx] = getattr(self, f"load{configC}")()
                except:
                    self.configs[idx] = self.loadConfig(config)
                config = self.configs[idx]
                try:
                    setattr(self, config.name, config.datas)
                except:
                    pass
                if self.dc.showLog:
                    print(f"done")
        if clean:
            self.cleanJson()

    def initConfigs(self):
        for idx, config in enumerate(self.configs):
            try:
                self.configs[idx] = getattr(self, f"init{self.dc.ownCapitalize(config.name)}")()
            except:
                self.configs[idx] = self.initConfig(config)

    def initConfig(self, config):
        path = os.path.join(self.basePath, f"{config.path}.json")

        if self.dc.downloadNewVersion:
            if self.dc.showLog:
                print(f"updating {config.name} ... ", end="")
            url = config.url.format(self.dc.version) if "version" in config.urlHint.split(" ") else config.url
            jsonData = saveJsonApiResponseInJsonFile(url, path)
            if self.dc.showLog:
                print("done")
        else:
            with open(path, "r") as f:
                jsonData = json.load(f)
        config.setJson(jsonData)
        return config

    def loadConfig(self, config):
        jsonDatas = config.json
        res = dict()
        if isinstance(jsonDatas, list):
            for elem in jsonDatas:
                k, v = self.getClassAsKeyClass(config, elem)
                config.addData(k, v)
        elif isinstance(jsonDatas, dict):
            for key, val in jsonDatas.items():
                k, v = self.getClassAsKeyClass(config, val, key)
                config.addData(k, v)
        return config

    def getDatas(self, configName):
        if configName in self.allConfig:
            return getattr(self, configName)
        return None

    def getPath(self, path):

        return os.path.join(self.basePath, path) if isinstance(path, str) else os.path.join(self.basePath, *path)
