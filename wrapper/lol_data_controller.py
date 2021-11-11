import json
import os

import requests

from wrapper.lol_wrapper import LolWrapper
from wrapper.tft_wrapper import TftWrapper


class LolDataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    downloadNewVersion = False
    basePath: str = "json_data"
    basePathVersions: str
    lol: LolWrapper = None
    tft: TftWrapper = None

    version = None

    def __init__(self, update=True, forceUpdate=False, showLog=False):
        self.showLog = showLog
        self.update = update
        self.forceUpdate = forceUpdate
        self.tft = TftWrapper(self)
        self.lol = LolWrapper(self)
        self.basePathVersions = os.path.join(self.basePath, "versions.json")
        self.checkVersion()
        # self.loadChampions()
        # self.loadItems()
        # self.loadScrawledItems()

    def checkVersion(self):
        try:
            with open(self.basePathVersions, "r") as f:
                self.version = json.load(f)[0]
        except:
            pass
        versions = requests.get(self.versionUrl).json()

        if self.version is None:
            self.version = versions[0]
        if self.forceUpdate:
            if self.showLog:
                print("/!\\ FORCE UPDATE /!\\")
            self.downloadNewVersion = True
        if versions[0] != self.version:
            if self.showLog:
                print('New Version Available')
            if self.update:
                self.downloadNewVersion = True

            elif not self.update and not self.forceUpdate:
                if self.showLog:
                    print("/!\\ UPDATE FALSE /!\\")
                self.downloadNewVersion = False
        if self.downloadNewVersion:
            with open(self.basePathVersions, "w+") as f:
                json.dump(versions, f)
