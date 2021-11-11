import json
import os
from typing import Dict

import requests
from dacite import from_dict
from scrapy.crawler import CrawlerProcess

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.gamemode import GameMode
from my_dataclass.lol.gametype import GameType
from my_dataclass.lol.item.item import Item
from my_dataclass.lol.map import Map
from my_dataclass.lol.queue import Queue
from my_dataclass.lol.season import Season
from my_dataclass.lol.summonerspell import SummonerSpell
from my_dataclass.lolapi.summoner.profileicon import ProfileIcon
from util.dataclass_function import ownCapitalize
from util.jsonfunction import saveJsonApiResponseInJsonFile
from scraper.lolDatas.spiders.lolfandom import LolfandomSpider
from my_dataclass.lol.item.itemcombined import ItemCombined
from wrapper.lolWrapper import LolWrapper
from wrapper.tftWrapper import TftWrapper


class LolDataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    downloadNewVersion = False
    basePath: str = "json_data"
    basePathVersions: str
    lol: LolWrapper = None
    tft: TftWrapper = None

    version = None

    def __init__(self, update=True, forceUpdate=False):
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
            print("/!\\ FORCE UPDATE /!\\")
            self.downloadNewVersion = True
        if versions[0] != self.version:

            print('New Version Available')
            if self.update:
                self.downloadNewVersion = True

            elif not self.update and not self.forceUpdate:
                print("/!\\ UPDATE FALSE /!\\")
                self.downloadNewVersion = False
        if self.downloadNewVersion:
            with open(self.basePathVersions, "w+") as f:
                json.dump(versions, f)
