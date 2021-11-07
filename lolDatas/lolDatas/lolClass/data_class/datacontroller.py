import json
import os

from dacite import from_dict

from lolDatas.lolClass.data_class.champion import Champion
from lolDatas.lolClass.data_class.item import Item
from lolDatas.lolClass.util.jsonfunction import saveJsonApiResponseInJsonFile


class DataController():
    versionUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    championsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json"
    itemsUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json"
    championInfoUrl = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json"
    downloadNewVersion = False
    basePath= ""
    champions = {}
    items = {}
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
    def __init__(self):
        print(os.getcwd())
        self.checkVersion()
        self.loadChampions()
        self.loadItems()

    def checkVersion(self):
        try:
            with open(self.basePath + "lolClass/json_data/version.json", "r") as f:
                self.version = json.load(f)[0]
        except:
            pass

        versions = saveJsonApiResponseInJsonFile(self.versionUrl, self.basePath + "lolClass/json_data/version.json")
        if self.version is None:
            self.version = versions[0]
        if versions[0] != self.version:
            self.downloadNewVersion = True
            print('Version differ , updating ...')

        else:
            print('Data up to Date')

    def itemParser(self, id_, item):
        newDict = dict(id=int(id_), name=item['name'], tags=item['tags'], armorPenFlat=0, magicPenFlat=0,
                       amorPenPercent=0, magicPenPercent=0, gold=item['gold']['total'])

        for k,v in self.itemKeys.items():
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
        newDict['mr'] = newDict['spellblock']
        newDict['mrperlevel'] = newDict['spellblockperlevel']
        newDict['ad'] = newDict['attackdamage']
        newDict['adperlevel'] = newDict['attackdamageperlevel']
        return from_dict(data_class=Champion, data=newDict)

    def loadChampions(self):
        if self.downloadNewVersion:
            self.championsJson = saveJsonApiResponseInJsonFile(self.championsUrl.format(self.version),
                                                               self.basePath + "lolClass/json_data/champions_light.json")

        else:
            with open(self.basePath + "lolClass/json_data/champions_light.json", "r") as f:
                self.championsJson = json.load(f)
        for champName, champion in self.championsJson['data'].items():
            if self.downloadNewVersion:
                champJson = saveJsonApiResponseInJsonFile(self.championInfoUrl.format(self.version, champName),
                                                          self.basePath + "lolClass/json_data/champions_advanced/{}.json".format(champName))
            else:
                with open(self.basePath + 'lolClass/json_data/champions_advanced/{}.json'.format(champName), "r") as f:
                    champJson = json.load(f)
            champ = self.champParser(champJson, champion)
            self.champions[champName] = champ

    def loadItems(self):
        if self.downloadNewVersion:
            self.itemsJson = saveJsonApiResponseInJsonFile(self.itemsUrl.format(self.version),
                                                           self.basePath + "lolClass/json_data/items.json")

        else:
            with open(self.basePath + "lolClass/json_data/items.json", "r") as f:
                self.itemsJson = json.load(f)

        for id_, itemJ in self.itemsJson['data'].items():
            self.items[id_] = self.itemParser(id_, itemJ)

    def getItemsNameAsUrl(self):
        return [item.name.replace(" ", "_") for k, item in self.items.items()]



if __name__ == '__main__':
    DataController().getItemsNameAsUrl()