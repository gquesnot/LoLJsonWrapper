import time

from my_dataclass.lol.game_mode import GameMode
from my_dataclass.lol.game_type import GameType
from my_dataclass.lol.item.item_combined import ItemCombined
from my_dataclass.lol.map import Map
from my_dataclass.lol.queue import Queue
from my_dataclass.lol.season import Season
from my_dataclass.lol.summoner_spell import SummonerSpell
from my_dataclass.lolapi.match.match import Match
from my_dataclass.lolapi.match_timeline.match_timeline import MatchTimeline
from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon
from my_dataclass.lolapi.summoner.rune import Rune
from my_dataclass.lolapi.summoner.rune_path import RunePath
from my_dataclass.lolapi.summoner.summoner import Summoner
from my_dataclass.tft.champion.champion import Champion as TftChampion
from my_dataclass.lol.champion.champion import Champion as LolChampion
from my_dataclass.tft.item.item import Item as TftItem
from my_dataclass.lol.item.item import Item as LolItem
from my_dataclass.tft.trait.trait import Trait
from util.init_lol_watcher import initLolWatcher
from wrapper.lol_data_controller import LolDataController

if __name__ == '__main__':
    ## init LolDataController with his default parameter look at the documentation for more info
    dc = LolDataController(update=True, forceUpdate=False, showLog=True)

    ## change jsonDownloadUrl in tftWrapper if new update and run the command below
    dc.tft.downloadJson()

    ## load method with his default parameter look at the documentation for more info
    ## load all lol dataclasses
    dc.lol.load(configsList=None, clean=True, withPickle=False, savePickle=False)  # without pickle : ~4.7s | with pickle ~0.019s
    ## load  all tft dataclasses
    dc.tft.load(configsList=None, clean=True, withPickle=False, savePickle=False)  # without pickle: ~0.02s | with pikle: ~0.001s

    ## LOL API
    lw = initLolWatcher()

    ## SummonerClass
    jsonSummoner = lw.summoner.by_name("euw1", "random Iron")
    summoner:Summoner = dc.lolApi.getSummoner(jsonSummoner)

    ## Match Class
    match = lw.match.by_id("EUROPE", "EUW1_5551190982")
    match:Match = dc.lolApi.getMatch(match)

    ## MatchTimeline class
    matchTimeline = lw.match.timeline_by_match("EUROPE", "EUW1_5551190982")
    matchTimeline: MatchTimeline = dc.lolApi.getMatchTimeline(matchTimeline)

    ## TFT

    ## Traits
    trait: Trait
    for traitName, trait in dc.tft.traits.items():
        print(traitName, trait)

    ## Items
    item: Item
    for itemId, item in dc.tft.items.items():
        print(itemId, item)

    # Champions
    champion: Champion
    for championName, champion in dc.tft.champions.items():
        print(championName, champion)

    ## LOL

    ## Champions
    champion: Champion
    for champName, champion in dc.lol.champions.items():
        print(f"{champName}:", "\n    - ".join([skin.name for skin in champion.skins]))

    ## Items from dragon json
    item: Item
    for itemId, item in dc.lol.items.items():
        print(item.id, item.name)

    ## Items combined
    itemCombined : ItemCombined
    for itemId, itemCombined, in dc.lol.itemsCombined.items():
        print(itemCombined.id, itemCombined.name)

    ## Runes
    rune: Rune
    for runeId, rune in dc.lol.runes.items():
        print(runeId, rune)

    ## Runes path
    runePath: RunePath
    for runePathId, runePath in dc.lol.runesPath.items():
        print(runePathId)
        for path in runePath.runes:

            for rune in path:
                print("    ",rune)
            print()

    ## ProfilIcons
    profileIcon: ProfileIcon
    for profileIconId, profileIcon in dc.lol.profileIcons.items():
        print(profileIconId, profileIcon)

    ## SummonerSpells
    summonerSpell: SummonerSpell
    for summonerSpellName, summonerSpell in dc.lol.summonerSpells.items():
        print(summonerSpellName, summonerSpell)

    ## Seasons
    season: Season
    for seasonId, season in dc.lol.seasons.items():
        print(seasonId, season)

    ## GameModes
    gameMode: GameMode
    for gameModeName, gameMode in dc.lol.gameModes.items():
        print(gameModeName, gameMode)

    ## GameTypes
    gameType: GameType
    for gameTypeName, gameType in dc.lol.gameTypes.items():
        print(gameTypeName, gameType)

    ## Maps
    map_: Map
    for mapId, map_ in dc.lol.maps.items():
        print(mapId, map_)

    ## Queues
    queue: Queue
    for queueId, queue in dc.lol.queues.items():
        print(queueId, queue)
