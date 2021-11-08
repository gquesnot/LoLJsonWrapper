import copy

from dataclasses import dataclass, field
from typing import List

import dacite

from lolDatas.lolDatas.lolClass.data_class.champion import Champion
from lolDatas.lolDatas.lolClass.data_class.event import Event
from lolDatas.lolDatas.lolClass.data_class.item import Item

statsChampToFix = [
    "hp",
    "hpperlevel",
    "hpregen",
    "hpregenperlevel",
    "mp",
    "mpperlevel",
    "mpregenperlevel",
    "mpregen",
    "armor",
    "armorperlevel",
    "mr",
    "mrperlevel",
    "attackspeed",
    "attackspeedperlevel",
    "ad",
    "adperlevel",
    "armorpen",
    "armorpenpercent",
    "magicpen",
    "magicpenpercent",
    "lifesteal",
    "omnivamp",
    "physicalvamp",
    "crit",
]
statsItemsToFix = [
    "hp",
    "hpregen",
    "armor",
    "ad",
    "ap",
    "mr",
    "movespeed",
    "movespeedpercent",
    "attackspeedpercent",
    "crit",
    "lifestealpercent",
    "armorpen",
    "armorpenpercent",
    "magicpenpercent",
    "magicpen",
]
statsParticipantToFix = [
    "dps",
    "dpsFrom",
    "adReductionFrom",
]


def fixChamp(champ):
    for k in statsChampToFix:
        if isinstance(champ[k], str):
            champ[k] = float(champ[k])
    return champ


def fixItems(items):
    for idx, item in enumerate(items):
        for k in statsItemsToFix:
            if isinstance(item[k], str):
                items[idx][k] = float(items[idx][k])

    return items


def rebuildPartcipant(participantDict):
    for k in statsParticipantToFix:
        if isinstance(participantDict[k], str):
            participantDict[k] = float(participantDict[k])

    participantDict['dps'] = float(participantDict['dps'])
    participantDict['dpsFrom'] = float(participantDict['dpsFrom'])
    participantDict['adReductionFrom'] = float(participantDict['adReductionFrom'])
    participantDict['items'] = fixItems(participantDict['items'])
    participantDict['modItems'] = fixItems(participantDict['modItems'])

    participantDict['champion'] = fixChamp(participantDict['champion'])
    participantDict['calculatedChamp'] = fixChamp(participantDict['calculatedChamp'])
    participant = dacite.from_dict(Participant, data=participantDict)
    return participant


def participantParser(dataFrame, dataInit, allFrames, dc):
    res = dict()
    res['id'] = int(dataFrame['participantId'])
    res['puuid'] = dataFrame['puuid']
    res['summonerName'] = dataInit['summonerName']
    res['win'] = dataInit['win']
    res['maxGold'] = dataInit['goldEarned']
    res['gold'] = 0
    res['teamId'] = int(dataInit['teamId'])
    itemsJson = [f"item{i}" for i in range(0, 7)]
    res['items'] = []
    res['items'] = [copy.deepcopy(dc.items[str(dataInit[itemName])]) for itemName in itemsJson if str(dataInit[itemName]) != "0" if "Trinket" not in dc.items[str(dataInit[itemName])].tags]

    res['events'] = [
        [event for event in frame['events'] if "participantId" in event.keys() and event['participantId'] == res["id"]]
        for frame in allFrames]

    res['modItems'] = []
    res['champion'] = copy.deepcopy(dc.champions[dataInit['championName']])
    res['calculatedChamp'] = copy.deepcopy(dc.champions[dataInit['championName']])
    participant = dacite.from_dict(Participant, data=res)
    return participant


@dataclass
class Participant:
    id: int
    puuid: str
    summonerName: str
    win: bool

    teamId: int
    items: list[Item]
    modItems: list[Item]
    champion: Champion
    events: List[List[Event]]
    calculatedChamp: Champion = field(default=None)
    gold: int = field(default=0)
    goldDiff: int = field(default=0)
    maxGold: int = field(default=0)
    dpsFrom: float = field(default=0)
    adReductionFrom: float = field(default=0)
    dps: float = field(default=0)
    level: int = field(default=0)

    def reset(self, resetItems):
        self.calculatedChamp = copy.deepcopy(self.champion)
        if resetItems:
            self.modItems = []




    def calculateItems(self):

        for item in self.modItems:
            self.calculatedChamp.addItemStat(item)

    def updateGold(self):
        self.goldDiff = self.gold
        for item in self.modItems:
            if isinstance(item, Item):
                gold = item.gold
            else:
                gold = item['gold']
            self.goldDiff -= gold

    def generateDps(self, me):

        armor = (self.calculatedChamp.armor * (1 - me.calculatedChamp.armorpenpercent)) - me.calculatedChamp.armorpen
        self.adReductionFrom = round(100 / (100 + armor), 2) * 100

        self.dpsFrom = round(me.dps * (self.adReductionFrom / 100), 2)
        # print(self.summonerName, me.summonerName, self.dpsFrom)


    def hasIE(self):
        for item in self.modItems:
            if item.id == 3031:
                return True
        return False
    def calculateItemsAndDps(self):
        self.reset(False)
        self.calculatedChamp.byLevel(self.level)
        self.updateGold()
        self.calculateItems()
        myAs = self.calculatedChamp.attackspeed if self.calculatedChamp.attackspeed <= 2.5 else 2.5
        self.dps = myAs * self.calculatedChamp.ad
        if self.calculatedChamp.crit != 0:
            critRatio = 0.75
            if self.hasIE():
                print("HAS IE")
                if self.calculatedChamp.crit >= 0.6:
                    critRatio = 1.15
            self.dps += (self.dps * critRatio)/ (1/self.calculatedChamp.crit)

    def updateFrameTo(self, participantFrame, endFrame, allItems,resetItems=True, show=False):
        if show:
            print("\n----\n")
        self.reset(resetItems)
        if resetItems:
            for frameEvents in self.events[:endFrame]:
                for event in frameEvents:

                    if event.type == "ITEM_PURCHASED":

                        itemId = str(event.itemId)
                        if itemId in allItems.keys():
                            if show:
                                print("buy ", allItems[itemId], f"at {event.timestamp}")
                            self.modItems.append(copy.deepcopy(allItems[itemId]))

                    elif event.type == "ITEM_DESTROYED":
                        itemId = str(event.itemId)
                        if itemId in allItems.keys():
                            if show:
                                print("destroyed ", allItems[itemId], f"at {event.timestamp}")
                            for idx, item in enumerate(self.modItems):
                                if item.id == event.itemId:
                                    del self.modItems[idx]
                                    break
        self.gold = participantFrame["totalGold"]
        self.level = participantFrame['level']
        self.calculatedChamp.byLevel(self.level)
        self.updateGold()
        self.calculateItems()
        myAs = self.calculatedChamp.attackspeed if self.calculatedChamp.attackspeed <= 2.5 else 2.5
        self.dps = myAs * self.calculatedChamp.ad
