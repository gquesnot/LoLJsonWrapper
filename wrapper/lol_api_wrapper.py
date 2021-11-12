from my_dataclass.lolapi.match.match import Match
from my_dataclass.lolapi.match_timeline.match_timeline import MatchTimeline
from my_dataclass.lolapi.summoner.summoner import Summoner
from util.base_api_wrapper import BaseApiWrapper


class LolApiWrapper(BaseApiWrapper):

    def __init__(self, dc):
        super().__init__(dc)

    def getSummoner(self, data) -> Summoner:
        return Summoner.from_dict(self.dc, data)

    def getMatch(self, match) -> Match:
        return Match.from_dict(self.dc, match)

    def getMatchTimeline(self, matchTimeline) -> MatchTimeline:
        return MatchTimeline.from_dict(self.dc, matchTimeline)
