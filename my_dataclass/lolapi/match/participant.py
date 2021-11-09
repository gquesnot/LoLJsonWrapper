from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.item.itemcombined import ItemCombined
from my_dataclass.lol.spell.summonerspell import SummonerSpell
from my_dataclass.lolapi.match.perk.perk import Perk
from my_dataclass.lolapi.summoner.summoner import Summoner


@dataclass
class MatchParticipant:
    perks: Perk
    champion: Champion#champion id -> Champion
    lane: Lane  # individualPosition +lane + role  + teamPosition  = lane -> Position / role
    profileIcon: Icon # icon Id -> Icon
    summoner: Summoner# summonerId summonerName -> Summoner
    summonerSpell1: SummonerSpell# summoner1Id summonerId1 cast ->
    summonerSpell2: SummonerSpell# summonerSpell2
    item0: ItemCombined # itemId -> Item
    item1: ItemCombined
    item2: ItemCombined
    item3: ItemCombined
    item4: ItemCombined
    item5: ItemCombined
    item6: ItemCombined
    assists: int = field(default=0)
    baronKills: int = field(default=0)
    bountyLevel: int = field(default=0)
    champExperience: int = field(default=0)
    champLevel: int = field(default=0)

    championTransform: int = field(default=0)
    consumablesPurchased: int = field(default=0)
    damageDealtToBuildings: int = field(default=0)
    damageDealtToObjectives: int = field(default=0)
    damageDealtToTurrets: int = field(default=0)
    damageSelfMitigated: int = field(default=0)
    deaths: int = field(default=0)
    detectorWardsPlaced: int = field(default=0)
    doubleKills: int = field(default=0)
    dragonKills: int = field(default=0)
    firstBloodAssist: float = field(default=False)
    firstBloodKill: float = field(default=False)
    firstTowerAssist: float = field(default=False)
    firstTowerKill: float = field(default=False)
    gameEndedInEarlySurrender: float = field(default=False)
    gameEndedInSurrender: float = field(default=False)
    goldEarned: int = field(default=0)
    goldSpent: int = field(default=0)

    inhibitorKills: int = field(default=0)
    inhibitorTakedowns: int = field(default=0)
    inhibitorsLost: int = field(default=0)

    itemsPurchased: int = field(default=0)
    killingSprees: int = field(default=0)
    kills: int = field(default=0)
    largestCriticalStrike: int = field(default=0)
    largestKillingSpree: int = field(default=0)
    largestMultiKill: int = field(default=0)
    longestTimeSpentLiving: int = field(default=0)
    magicDamageDealt: int = field(default=0)
    magicDamageDealtToChampions: int = field(default=0)
    magicDamageTaken: int = field(default=0)
    neutralMinionsKilled: int = field(default=0)
    nexusKills: int = field(default=0)
    nexusLost: bool = field(default=False)
    nexusTakedowns: bool = field(default=False)
    objectivesStolen: int = field(default=0)
    objectivesStolenAssists: int = field(default=0)
    id: int = field(default=None)
    pentaKills: int = field(default=0)
    physicalDamageDealt: int = field(default=0)
    physicalDamageDealtToChampions: int = field(default=0)
    physicalDamageTaken: int = field(default=0)

    puuid: str = field(default=None)
    quadraKills: int = field(default=0)
    riotIdName: str = field(default="")
    riotIdTagline: str = field(default="")
    sightWardsBoughtInGame: int = field(default=0)
    spell1Casts: int = field(default=0)
    spell2Casts: int = field(default=0)
    spell3Casts: int = field(default=0)
    spell4Casts: int = field(default=0)
    summoner1Casts: int = field(default=0)

    summoner2Casts: int = field(default=None)

    teamEarlySurrendered: bool = field(default=False)
    teamId: int = field(default=None)
    timeCCingOthers: int = field(default=0)
    timePlayed: int = field(default=0)
    totalDamageDealt: int = field(default=0)
    totalDamageDealtToChampions: int = field(default=0)
    totalDamageShieldedOnTeammates: int = field(default=0)
    totalDamageTaken: int = field(default=0)
    totalHeal: int = field(default=0)
    totalHealsOnTeammates: int = field(default=0)
    totalMinionsKilled: int = field(default=0)
    totalTimeCCDealt: int = field(default=0)
    totalTimeSpentDead: int = field(default=0)
    totalUnitsHealed: int = field(default=0)
    tripleKills: int = field(default=0)
    trueDamageDealt: int = field(default=0)
    trueDamageDealtToChampions: int = field(default=0)
    trueDamageTaken: int = field(default=0)
    turretKills: int = field(default=0)
    turretTakedowns: int = field(default=0)
    turretsLost: int = field(default=0)
    unrealKills: int = field(default=0)
    visionScore: int = field(default=0)
    visionWardsBoughtInGame: int = field(default=0)
    wardsKilled: int = field(default=0)
    wardsPlaced: int = field(default=0)
    win: bool = field(default=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MatchParticipant":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
