import json
import os

import requests

from util.dataclass_function import ownCapitalize
from wrapper.lol_api_wrapper import LolApiWrapper
from wrapper.lol_json_wrapper import LolJsonWrapper
from wrapper.tft_json_wrapper import TftJsonWrapper


class LolDataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    downloadNewVersion = False
    basePath: str = "json_data"
    picklePath: str = "pickle"
    basePathVersions: str
    lol: LolJsonWrapper = None
    tft: TftJsonWrapper = None
    lolApi: LolApiWrapper = None

    version = None

    def __init__(self, update=True, forceUpdate=False, showLog=False):
        """

        :param update: if lol update will update
        :param forceUpdate: force update
        :param showLog: show info about loading etc
        """
        self.showLog = showLog
        self.update = update
        self.ownCapitalize = ownCapitalize
        self.forceUpdate = forceUpdate
        self.tft = TftJsonWrapper(self)
        self.lol = LolJsonWrapper(self)

        self.lolApi = LolApiWrapper(self)
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
