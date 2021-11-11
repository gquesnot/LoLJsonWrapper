import json
import os
from typing import Dict

from dacite import from_dict
from scrapy.crawler import CrawlerProcess


from my_dataclass.lol.item.item_combined import ItemCombined
from my_dataenum.config_index import ConfigIndex
from scraper.lolDatas.spiders.lolfandom import LolfandomSpider
from util.json_function import saveJsonApiResponseInJsonFile, getJson
from util.base_wrapper import BaseWrapper
from util.base_wrapper_function import  getItemsNameAsUrl, withoutDataDict
from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.game_mode import GameMode
from my_dataclass.lol.game_type import GameType
from my_dataclass.lol.item.item import Item
from my_dataclass.lol.map import Map
from my_dataclass.lol.queue import Queue
from my_dataclass.lol.season import Season
from my_dataclass.lol.summoner_spell import SummonerSpell
from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon


class LolWrapper(BaseWrapper):
    hint = "lol"

    configsDict = [
        {
            "name": "profileIcons",
            "path": "profile_icons",
            "class_": ProfileIcon,
            "url": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/profileicon.json",
            "urlHint": "version",
            "configIndex": ConfigIndex.ID
        },
        {
            "name": "summonerSpells",
            "path": "summoner_spells",
            "class_": SummonerSpell,
            "url": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/summoner.json",
            "urlHint": "version",

        },
        {
            "name": "seasons",
            "class_": Season,
            "url": "https://static.developer.riotgames.com/docs/lol/seasons.json",
            "configIndex": ConfigIndex.ID
        },
        {
            "name": "gameModes",
            "path": "game_modes",
            "class_": GameMode,
            "url": "https://static.developer.riotgames.com/docs/lol/gameModes.json",
            "configIndex": ConfigIndex.NAME
        },
        {
            "name": "gameTypes",
            "path": "game_types",
            "class_": GameType,
            "url": "https://static.developer.riotgames.com/docs/lol/gameTypes.json",
            "configIndex": ConfigIndex.NAME
        },
        {
            "name": "maps",
            "class_": Map,
            "url": "https://static.developer.riotgames.com/docs/lol/maps.json",
            "configIndex": ConfigIndex.ID
        },
        {
            "name": "queues",
            "class_": Queue,
            "url": "https://static.developer.riotgames.com/docs/lol/queues.json",
        },
        {
            "name": "champions",
            "class_": Champion,
            "url": ["http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json",
                    "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"]
        },
        {
            "name": "items",
            "class_": Item,
            "url": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json",
            "urlHint": "version"
        },
        {
            "name": "itemsCombined",
            "path": "items_combined",
            "class_": ItemCombined,
        },
    ]

    itemsCrawlJson = {}
    profileIcons: Dict[str, ProfileIcon]
    summonerSpells: Dict[str, SummonerSpell]
    seasons: Dict[str, Season]
    gameModes: Dict[str, GameMode]
    gameTypes: Dict[str, GameType]
    maps: Dict[str, Map]
    queues: Dict[str, Queue]
    champions: Dict[str, Champion]
    items: Dict[str, Item]
    itemsCombined: Dict[str, ItemCombined]



    def __init__(self, dc):
        super().__init__(dc)

    def loadQueues(self):

        configQueues = self.getConfigByName("queues")
        maps = self.getConfigByName("maps").datas
        for queue_ in configQueues.json:
            myMap = maps[queue_['map']] if queue_['map'] in maps else None
            sQueue = Queue.from_dict(queue_, myMap)
            configQueues.addData(str(sQueue.id), sQueue)

        return configQueues

    def initChampions(self):
        config = self.getConfigByName("champions")
        path = self.getPath(f"champion_light.json")
        if self.dc.downloadNewVersion:

            if self.dc.showLog:
                print("updating lol champions ... ", end="")
            championsJsonLight = withoutDataDict(saveJsonApiResponseInJsonFile(config.url[0].format(self.dc.version), path))
            if self.dc.showLog:
                print("done")

        else:
            championsJsonLight = withoutDataDict(getJson("champions_light", self.basePath))

        config.setJson(championsJsonLight)
        championsJsonFull = dict()
        for champName, champion in championsJsonLight.items():
            path = self.getPath(["champions_full", f"{champName}.json"])

            if self.dc.downloadNewVersion:
                championsJsonFull[champName] = withoutDataDict(saveJsonApiResponseInJsonFile(
                    config.url[1].format(self.dc.version, champName), path))
            else:
                championsJsonFull[champName] = withoutDataDict(
                    getJson(champName, os.path.join(self.basePath, "champions_full")))
        config.setJson(championsJsonFull)
        return config

    def loadChampions(self):
        config = self.getConfigByName("champions")
        for champName, champFull, champLight in zip(config.json[1].keys(), config.json[1].values(), config.json[0].values()):
            config.addData(champName, Champion.from_dict(champFull, champLight))
        return config

    def loadItems(self):
        config = self.getConfigByName("items")
        for id_, itemJ in config.json.items():
            config.addData(id_,  config.class_.from_dict(id_, itemJ))
        return config

    def initItemsCombined(self):

        config = self.getConfigByName("itemsCombined")
        crawlPath = self.getPath("items_crawl.json")
        combinedPath = self.getPath("items_combined.json")

        if self.dc.downloadNewVersion:
            if self.dc.showLog:
                print("updating crawled items ... ")
            self.crawlItems(crawlPath)
            with open(crawlPath, "r") as f:
                self.itemsCrawlJson = json.load(f)
        else:
            with open(crawlPath, "r") as f:
                self.itemsCrawlJson = json.load(f)
            with open(combinedPath, "r") as f:
                config.setJson(json.load(f))
        return config

    def loadItemsCombined(self):
        config = self.getConfigByName("itemsCombined")
        if self.dc.downloadNewVersion:
            config.datas = self.combineItems()
        else:
            for k, v in config.json.items():
                config.addData(k,from_dict(ItemCombined, v))
        return config

    def combineItems(self):
        resItems = dict()
        configItems = self.getConfigByName("items")
        configItemsCombined = self.getConfigByName("itemsCombined")
        configChampions = self.getConfigByName("champions")
        path = self.getPath(f"{configItemsCombined.path}.json")
        for itemId, item in configItems.json.items():
            for item_crawl in self.itemsCrawlJson:
                if item['name'] == item_crawl['name']:
                    configItemsCombined.addData(itemId, ItemCombined.from_dict(itemId,  item_crawl, configChampions.datas,item))
        with open(path, "w+") as f:
            json.dump({k: v.to_dict() for k, v in resItems.items()}, f)
        return resItems

    def crawlItems(self, crawlPath):
        try:
            os.remove(crawlPath)
        except:
            pass

        process = CrawlerProcess(settings={
            "FEEDS": {
                crawlPath: {"format": "json"},
            },
        })

        process.crawl(LolfandomSpider, itemsName=getItemsNameAsUrl(self.getConfigByName("items").json))
        process.start()
        process.join()


