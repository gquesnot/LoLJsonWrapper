import copy
import json
import os
from typing import List, Dict

import requests
from dacite import from_dict
from scrapy.crawler import CrawlerProcess

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.item.item import Item
from util.dataclass_function import ownCapitalize
from util.jsonfunction import saveJsonApiResponseInJsonFile
from scraper.lolDatas.spiders.lolfandom import LolfandomSpider
from my_dataclass.lol.item.itemcombined import ItemCombined


class LolDataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    championsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json"
    itemsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json"
    championInfoUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"
    downloadNewVersion = False
    basePath = "json_data/"
    mappedLoading = {
        "lol": [
            "champions",
            "items",
            "itemsCombined"
        ],
        "tft": [
            "champions",
            "items",
            "traits"
        ]

    }

    champions: Dict[str, Champion] = {}
    items: Dict[str, Item] = {}
    itemsJson = {}
    championsJsonLight = {}
    championsJsonFull = {}
    itemsCombined: Dict[str, ItemCombined] = {}
    itemsCrawlJson = []
    itemsCombinedJson = {}
    itemKeys = {
        "hp": "FlatHPPoolMod",
        "mp": "FlatMPPoolMod",
        "hpregen": "FlatHPRegenMod",
        "armor": "FlatArmorMod",
        "ad": "FlatPhysicalDamageMod",
        "ap": "FlatMagicDamageMod",
        "mr": "FlatSpellBlockMod",
        "ms": "FlatMovementSpeedMod",
        "msPercent": "PercentMovementSpeedMod",
        "attackSpeedPercent": "PercentAttackSpeedMod",
        "crit": "FlatCritChanceMod",
        "lifeStealPercent": "PercentLifeStealMod",
    }
    version = None

    def __init__(self, update=True, forceUpdate=False):
        self.update = update
        self.forceUpdate = forceUpdate
        self.checkVersion()
        # self.loadChampions()
        # self.loadItems()
        # self.loadScrawledItems()

    def checkVersion(self):
        try:
            with open(self.basePath + "versions.json", "r") as f:
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
            with open(self.basePath + "versions.json", "w+") as f:
                json.dump(versions, f)

    def itemParser(self, id_, item):
        newDict = dict(id=int(id_), name=item['name'], tags=item['tags'], armorPenFlat=0, magicPenFlat=0,
                       amorPenPercent=0, magicPenPercent=0, gold=item['gold']['total'])

        for k, v in self.itemKeys.items():
            if v in item['stats'].keys():
                if k == 'movementspeedpercent':
                    newDict[k] = float(item['stats'][v])
                else:
                    newDict[k] = item['stats'][v]

        for i, tag in enumerate(item['tags']):
            if tag in ("MagicPenetration", "ArmorPenetration"):
                if "effect" in item.keys():
                    effectStr = "Effect{}Amount".format(i + 1)
                    if effectStr in item['effect'].keys():
                        value = float(item['effect'][effectStr])
                        isPercent = value < 1

                        if tag == "MagicPenetration":
                            if isPercent:
                                newDict['magicpenpercent'] = value
                            else:
                                newDict['magicpen'] = value
                        elif tag == "ArmorPenetration":
                            if isPercent:
                                newDict['armorpenpercent'] = value
                            else:
                                newDict['armorpen'] = value

        return from_dict(data_class=Item, data=newDict)

    def champParser(self, champJson, champion):

        return

    def initLolChampions(self):
        if self.downloadNewVersion:
            print("updating lol champions ... ")
            self.championsJsonLight = saveJsonApiResponseInJsonFile(self.championsUrl.format(self.version),
                                                                    self.basePath + "champions_light.json")['data']

        else:
            with open(self.basePath + "champions_light.json", "r") as f:
                self.championsJsonLight = json.load(f)['data']
        for champName, champion in self.championsJsonLight.items():
            if self.downloadNewVersion:
                self.championsJsonFull[champName] = saveJsonApiResponseInJsonFile(
                    self.championInfoUrl.format(self.version, champName),
                    self.basePath + "champions_full/{}.json".format(
                        champName))['data']
            else:
                with open(self.basePath + 'champions_full/{}.json'.format(champName), "r") as f:
                    self.championsJsonFull[champName] = json.load(f)['data']

    def loadLolChampions(self):
        for champName, champFull in self.championsJsonFull.items():
            champLight = self.championsJsonLight[champName]
            self.champions[champName] = Champion.from_dict(champFull, champLight)

    def initLolItems(self):
        if self.downloadNewVersion:
            print("updating items ... ")
            self.itemsJson = saveJsonApiResponseInJsonFile(self.itemsUrl.format(self.version),
                                                           self.basePath + "items.json")['data']
        else:
            with open(self.basePath + "items.json", "r") as f:
                self.itemsJson = json.load(f)['data']

    def loadLolItems(self):
        for id_, itemJ in self.itemsJson.items():
            self.items[id_] = self.itemParser(id_, itemJ)

    def getItemsNameAsUrl(self):

        return [item['name'].replace(" ", "_") for k, item in self.itemsJson.items()]

    def initLolCrawledItems(self):
        if self.downloadNewVersion:
            print("updating crawled items ... ")
            self.crawlItems()
            with open(self.basePath + "items_crawl.json", "r") as f:
                self.itemsCrawlJson = json.load(f)
        else:
            with open(self.basePath + "items_crawl.json", "r") as f:
                self.itemsCrawlJson = json.load(f)
            with open(self.basePath + "items_combined.json", "r") as f:
                self.itemsCombinedJson = json.load(f)

    def loadLolItemsCombined(self):
        if self.downloadNewVersion:
            self.itemsCombined = self.combineItems()
        else:
            for k, v in self.itemsCombinedJson.items():
                self.itemsCombined[k] = from_dict(ItemCombined, v)

    def crawlItems(self):
        try:
            os.remove(self.basePath + "items_crawl.json")
        except:
            pass

        process = CrawlerProcess(settings={
            "FEEDS": {
                self.basePath + "items_crawl.json": {"format": "json"},
            },
        })

        process.crawl(LolfandomSpider, itemsName=self.getItemsNameAsUrl())
        process.start()
        process.join()

    def fieldMappingCrawlItem(self, itemId, dataItem, crawlItem):
        dataItem['id'] = int(itemId)
        dataItem['stats'] = {k: v for k, v in crawlItem.items() if k != "name"}
        for k, v in dataItem['stats'].items():
            if "percent" in k and v is not None:
                dataItem['stats'][k] = round(v / 100, 2)
        if "requiredChampion" in dataItem.keys():
            champName = dataItem["requiredChampion"]
            champion = None
            if champName not in self.champions.keys():

                if champName.capitalize() not in self.champions.keys():
                    print("ERRROR")
                else:
                    champion = self.champions[champName.capitalize()]
            else:
                champion = self.champions[champName]

            dataItem["requiredChampion"] = champion
        if "specialRecipe" in dataItem.keys():
            dataItem["specialRecipe"] = int(dataItem['specialRecipe'])

        dataItem['maps'] = [int(mapId) for mapId, v in dataItem['maps'].items() if v]
        return dataItem

    def load(self, hint="lol", configs=None):
        if hint in self.mappedLoading.keys():
            allConfig = self.mappedLoading[hint]
            if configs is not None:
                hasError = len([1 for config in configs if config not in allConfig]) != 0
                if hasError:
                    print("HAS ERROR IN CONFIG")
                    return
            else:
                configs = allConfig
            hintC = ownCapitalize(hint)
            print(f"init {hint} datas ...", end="")
            # init function
            getattr(self, f"init{hintC}")()
            print(f" done")
            for config in allConfig:

                if config in configs:
                    configC = ownCapitalize(config)
                    print(f"loading {hint} {config} ...", end="")
                    # load function
                    getattr(self, f"load{hintC}{configC}")()
                    print(" done")
        else:
            print("HAS ERROR IN HINT")

    def initLol(self):
        self.initLolChampions()
        self.initLolItems()
        self.initLolCrawledItems()

    def initTft(self):
        self.initTftChampions()
        self.initTftItems()
        self.initTftTraits()

    def combineItems(self):
        resItems = dict()
        for itemId, item in self.itemsJson.items():
            for item_crawl in self.itemsCrawlJson:
                if item['name'] == item_crawl['name']:
                    data = self.fieldMappingCrawlItem(itemId, item, item_crawl)

                    resItems[itemId] = ItemCombined.from_dict(data)
        with open(self.basePath + "items_combined.json", "w+") as f:
            json.dump({k: v.to_dict() for k, v in resItems.items()}, f)
        return resItems

    def initTftChampions(self):
        pass

    def initTftItems(self):
        pass

    def initTftTraits(self):
        pass
