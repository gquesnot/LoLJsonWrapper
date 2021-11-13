import json
import os
from typing import Dict, Union

from dacite import from_dict
from scrapy.crawler import CrawlerProcess

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.game_mode import GameMode
from my_dataclass.lol.game_type import GameType
from my_dataclass.lol.item.item import Item
from my_dataclass.lol.item.item_combined import ItemCombined
from my_dataclass.lol.map import Map
from my_dataclass.lol.queue import Queue
from my_dataclass.lol.season import Season
from my_dataclass.lol.summoner_spell import SummonerSpell
from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon
from my_dataclass.lolapi.summoner.rune import Rune
from my_dataclass.lolapi.summoner.rune_path import RunePath
from my_dataenum.config_index import ConfigIndex
from scraper.lolDatas.spiders.lolfandom import LolfandomSpider
from util.base_json_wrapper import BaseJsonWrapper
from util.base_wrapper_function import getItemsNameAsUrl, withoutDataDict
from util.json_function import saveJsonApiResponseInJsonFile, getJson


class LolJsonWrapper(BaseJsonWrapper):
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
            "configIndex": ConfigIndex.ID,
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
        {
            "name": "runesPath",
            "path": "runes_reforged",
            "url": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/runesReforged.json",
            "class_": RunePath,
            "urlHint": "version"
        }
    ]

    itemsCrawlJson = {}
    missingConfigToPickle = ["runes"]
    profileIcons: Dict[str, ProfileIcon] = dict()
    summonerSpells: Dict[str, SummonerSpell] = dict()
    seasons: Dict[str, Season] = dict()
    gameModes: Dict[str, GameMode] = dict()
    gameTypes: Dict[str, GameType] = dict()
    maps: Dict[str, Map] = dict()
    queues: Dict[str, Queue] = dict()
    champions: Dict[str, Champion] = dict()
    items: Dict[str, Item] = dict()
    itemsCombined: Dict[str, ItemCombined] = dict()
    runesPath: Dict[str, RunePath] = dict()
    runes: Dict[str, Union[Rune, RunePath]] = dict()

    def __init__(self, dc):
        super().__init__(dc)




    def loadRunesPath(self):
        config = self.getConfigByName("runesPath")

        for path in config.json:
            runesSlots = []
            for slot in path['slots']:
                newRunes = []
                for rune in slot['runes']:
                    myRune = Rune.from_dict(rune)
                    newRunes.append(myRune.to_dict())
                    self.runes[str(myRune.id)] = myRune
                runesSlots.append(newRunes)
            myRunePath = RunePath.from_dict(path, runesSlots)
            self.runesPath[str(myRunePath.id)] = myRunePath
            config.datas = self.runesPath
        return config

    def initChampions(self):
        config = self.getConfigByName("champions")
        path = self.getPath(f"champions_light.json")
        if self.dc.downloadNewVersion:

            if self.dc.showLog:
                print("updating lol champions ... ", end="")
            championsJsonLight = withoutDataDict(
                saveJsonApiResponseInJsonFile(config.url[0].format(self.dc.version), path))
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
        for champName, champFull, champLight in zip(config.json[1].keys(), config.json[1].values(),
                                                    config.json[0].values()):
            config.addData(champName, Champion.from_dict(self.dc, champFull, champLight))
        return config

    def loadItems(self):
        config = self.getConfigByName("items")
        for id_, itemJ in config.json.items():
            config.addData(id_, Item.from_dict(id_, itemJ))
        return config

    def getChampById(self, id_):
        for champName, champ in self.champions.items():
            if champ.id == id_:
                return champ
        return None

    def getSummonerSpellById(self, id_):
        for summonerSpellName, summonerSpell in self.summonerSpells.items():
            if summonerSpell.id == id_:
                return summonerSpell
        return None

    def initItemsCombined(self):

        config = self.getConfigByName("itemsCombined")
        crawlPath = self.getPath("items_crawl.json")
        combinedPath = self.getPath("items_combined.json")

        if self.dc.downloadNewVersion:
            if self.dc.showLog:
                print("updating crawled items ... ")
            # self.crawlItems(crawlPath)
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
                config.addData(k, from_dict(ItemCombined, v))
        return config

    def getItemsById(self, id_):

        id_ = str(id_) if isinstance(id_, int) else id_
        if id_ == 0:
            return None
        if id_ in self.itemsCombined.keys():
            return self.itemsCombined[id_]
        elif id_ in self.items.keys():
            return self.items[id_]
        else:
            return None

    def combineItems(self):
        resItems = dict()
        configItems = self.getConfigByName("items")
        configItemsCombined = self.getConfigByName("itemsCombined")
        configChampions = self.getConfigByName("champions")
        path = self.getPath(f"{configItemsCombined.path}.json")
        for itemId, item in configItems.json.items():
            for item_crawl in self.itemsCrawlJson:
                if item['name'] == item_crawl['name']:
                    configItemsCombined.addData(itemId,
                                                ItemCombined.from_dict(itemId, item_crawl, configChampions.datas, item))
        with open(path, "w+") as f:
            json.dump({k: v.to_dict() for k, v in configItemsCombined.datas.items()}, f)
        return configItemsCombined.datas

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
