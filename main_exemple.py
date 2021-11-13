import time

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
    summonerClass = dc.lolApi.getSummoner(jsonSummoner)

    ## Match Class
    match = lw.match.by_id("EUROPE", "EUW1_5551190982")
    matchClass = dc.lolApi.getMatch(match)

    ## MatchTimeline class
    matchTimeline = lw.match.timeline_by_match("EUROPE", "EUW1_5551190982")
    matchTimelineClass = dc.lolApi.getMatchTimeline(matchTimeline)

    ## TFT

    ## Traits

    for traitName, trait in dc.tft.traits.items():
        print(traitName, trait)

    ## Items
    for itemId, item in dc.tft.items.items():
        print(itemId, item)

    # Champions
    for championName, champion in dc.tft.champions.items():
        print(championName, champion)

    ## LOL

    ## Champions
    for champName, champion in dc.lol.champions.items():
        print(f"{champName}:", "\n    - ".join([skin.name for skin in champion.skins]))

    ## Items from dragon json
    for itemId, item in dc.lol.items.items():
        print(item.id, item.name)

    ## Items combined
    for itemId, itemCombined, in dc.lol.itemsCombined.items():
        print(itemCombined.id, itemCombined.name)

    ## Runes
    for runeId, rune in dc.lol.runes.items():
        print(runeId, rune)

    ## Runes path
    for runePathId, runePath in dc.lol.runesPath.items():
        print(runePathId)
        for path in runePath.runes:

            for rune in path:
                print("    ",rune)
            print()

    ## ProfilIcons
    for profilIconId, profilIcon in dc.lol.profileIcons.items():
        print(profilIconId, profilIcon)

    ## SummonerSpells
    for summonerSpellName, summonerSpell in dc.lol.summonerSpells.items():
        print(summonerSpellName, summonerSpell)

    ## Seasons
    for seasonId, season in dc.lol.seasons.items():
        print(seasonId, season)

    ## GameModes
    for gameModeName, gameMode in dc.lol.gameModes.items():
        print(gameModeName, gameMode)

    ## GameTypes
    for gameTypeName, gameType in dc.lol.gameTypes.items():
        print(gameTypeName, gameType)

    ## Maps
    for mapId, map_ in dc.lol.maps.items():
        print(mapId, map_)

    ## Queues
    for queueId, queue in dc.lol.queues.items():
        print(queueId, queue)
