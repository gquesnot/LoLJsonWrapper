import copy
import json
import os

import dacite
import requests
from dacite import from_dict
from scrapy.crawler import CrawlerProcess

from lolClass.data_class.champion import Champion
from lolClass.data_class.item import Item
from lolClass.util.jsonfunction import saveJsonApiResponseInJsonFile
from lolDatas.lolDatas.spiders.lolfandom import LolfandomSpider
from new_data_class.item import Item as CombinedItem


class LolDataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    championsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json"
    itemsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json"
    championInfoUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"
    downloadNewVersion = False
    basePath = "lolClass/json_data/"
    champions = {}
    items = {}
    itemsJson = {}

    itemsCombined = {}
    itemsCrawlJson = []
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
        self.loadChampions()
        self.loadItems()
        self.loadScrawledItems()

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
            print("Updating ...")

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

        newDict = {"name": champion['name']} | champion['stats']
        newDict['id'] = int(champion['key'])
        newDict['mr'] = newDict['spellblock']
        newDict['mrperlevel'] = newDict['spellblockperlevel']
        newDict['ad'] = newDict['attackdamage']
        newDict['adperlevel'] = newDict['attackdamageperlevel']
        return from_dict(data_class=Champion, data=newDict)

    def loadChampions(self):
        if self.downloadNewVersion:
            self.championsJson = saveJsonApiResponseInJsonFile(self.championsUrl.format(self.version),
                                                               self.basePath + "champions_light.json")

        else:
            with open(self.basePath + "champions_light.json", "r") as f:
                self.championsJson = json.load(f)
        for champName, champion in self.championsJson['data'].items():
            if self.downloadNewVersion:
                champJson = saveJsonApiResponseInJsonFile(self.championInfoUrl.format(self.version, champName),
                                                          self.basePath + "champions_advanced/{}.json".format(
                                                              champName))
            else:
                with open(self.basePath + 'champions_advanced/{}.json'.format(champName), "r") as f:
                    champJson = json.load(f)
            champ = self.champParser(champJson, champion)
            self.champions[champName] = champ

    def loadItems(self):
        if self.downloadNewVersion:
            self.itemsJson = saveJsonApiResponseInJsonFile(self.itemsUrl.format(self.version),
                                                           self.basePath + "items.json")

        else:
            with open(self.basePath + "items.json", "r") as f:
                self.itemsJson = json.load(f)

        for id_, itemJ in self.itemsJson['data'].items():
            self.items[id_] = self.itemParser(id_, itemJ)

    def getItemsNameAsUrl(self):
        return [item.name.replace(" ", "_") for k, item in self.items.items()]

    def loadScrawledItems(self):

        if self.downloadNewVersion:
            self.crawlItems()
            with open(self.basePath + "items_crawl.json", "r") as f:
                self.itemsCrawlJson = json.load(f)
            self.itemsCombined = self.combineItems()
        else:
            with open(self.basePath + "items_crawl.json", "r") as f:
                self.itemsCrawlJson = json.load(f)
            with open(self.basePath + "items_combined.json", "r") as f:
                self.itemsCombined = json.load(f)

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

    def fieldMappingCrawlItem(self, dataItem, crawlItem):
        res = dict()
        dataItem['stats'] = {k: v for k, v in crawlItem.items() if k != "name"}
        for k,v in dataItem['stats'].items():
            if "percent" in k and v is not None:
                dataItem['stats'][k] = round(v/100,2)
        if "requiredChampion" in dataItem.keys():
            champName = dataItem["requiredChampion"]
            champion = None
            if champName not in self.champions.keys():

                if champName.capitalize() not in self.champions.keys():
                    print("ERRROR")
                else:
                    champion = copy.deepcopy(self.champions[champName.capitalize()])
            else:
                champion = copy.deepcopy(self.champions[champName])

            dataItem["requiredChampion"] = copy.deepcopy(champion)
        dataItem['maps'] = [int(mapId) for mapId, v in dataItem['maps'].items() if v]
        return dataItem

    def combineItems(self):
        resItems = dict()
        for itemId, item in self.itemsJson['data'].items():
            for item_crawl in self.itemsCrawlJson:
                if item['name'] == item_crawl['name']:
                    data = self.fieldMappingCrawlItem(item, item_crawl)

                    resItems[itemId] = CombinedItem.from_dict(data)
        with open(self.basePath + "items_combined.json", "w+") as f:
            json.dump({k: v.to_dict() for k, v in resItems.items()}, f)
        return resItems
