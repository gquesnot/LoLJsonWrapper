import time

from util.init_lol_watcher import initLolWatcher
from wrapper.lol_data_controller import LolDataController

if __name__ == '__main__':
    dc = LolDataController(update=True, forceUpdate=False, showLog=True)

    dc.lol.load()
    dc.tft.load()

    lw = initLolWatcher()

    # jsonSummoner = lw.summoner.by_name("euw1", "random Iron")

    # SummonerClass
    # summonerClass = dc.lolApi.getSummoner(jsonSummoner)

    # match = lw.match.by_id("EUROPE", "EUW1_5551190982")
    # # Match Class
    # matchClass = dc.lolApi.getMatch(match)
    # print(match.gameInfo.team1)
    # print(match.gameInfo.team2)

    # MatchTimeline class
    # matchTimeline = lw.match.timeline_by_match("EUROPE", "EUW1_5551190982")
    # matchTimelineClass = dc.lolApi.getMatchTimeline(matchTimeline)