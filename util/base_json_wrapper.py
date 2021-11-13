from __future__ import annotations

import json
import os.path
import pickle
import time
from typing import List

from util.json_wrapper_config import JsonWrapperConfig
from util.base_wrapper import BaseWrapper
from util.json_function import saveJsonApiResponseInJsonFile


class BaseJsonWrapper(BaseWrapper):
    configs: List[JsonWrapperConfig]
    basePath: str
    missingConfigToPickle: List[str] = []

    def __init__(self, dc):
        self.configs = [JsonWrapperConfig.from_dict(idx, config) for idx, config in enumerate(self.configsDict)]
        super().__init__(dc)
        self.basePath = os.path.join(self.dc.basePath, self.hint)

    def load(self, configsList=None, clean: bool = True, withPickle: bool = False, savePickle: bool = False):
        """
        :param configsList:
        :param clean: clean json
        :param withPickle: load from pickle
        :param savePickle: load and save pickle
        :return: None
        """
        t = time.time()
        if withPickle:
            self.loadPickle()
        else:
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
                    if len(config.datas.keys()) == 0:
                        print(f"ERROR config {config.name}")
                    setattr(self, config.name, config.datas)

                    if self.dc.showLog:
                        print(f"done")
            if clean:
                self.cleanJson()
        if self.dc.showLog:
            print("\n{}  data loaded in {}s\n".format(self.hint.upper(), round(time.time() - t, 3)))
        if savePickle:
            self.savePickle()

    def initConfigs(self):
        for idx, config in enumerate(self.configs):
            try:
                self.configs[idx] = getattr(self, f"init{self.dc.ownCapitalize(config.name)}")()
            except:
                self.configs[idx] = self.initConfig(config)

    def initConfig(self, config):
        path = os.path.join(self.basePath, f"{config.path}.json")
        print(path)

        if self.dc.downloadNewVersion and config.url is not None:
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

    def loadPickle(self):

        for config in self.configs:
            path = os.path.join(self.dc.picklePath, self.hint, config.path)
            if not os.path.isfile(path):
                print(f"ERROR PICKLE {config.name} NOT FOUND")
            else:
                with open(path, "rb") as f:
                    setattr(self, config.name, pickle.load(f))

        for attrName in self.missingConfigToPickle:
            path = os.path.join(self.dc.picklePath, self.hint, attrName)
            with open(path, "rb") as f:
                setattr(self, attrName, pickle.load(f))

    def savePickle(self):

        for config in self.configs:
            path = os.path.join(self.dc.picklePath, self.hint, config.path)
            with open(path, "wb") as f:
                pickle.dump(getattr(self, config.name), f)
        for attrName in self.missingConfigToPickle:
            path = os.path.join(self.dc.picklePath, self.hint, attrName)
            with open(path, "wb") as f:
                pickle.dump(getattr(self, attrName), f)
