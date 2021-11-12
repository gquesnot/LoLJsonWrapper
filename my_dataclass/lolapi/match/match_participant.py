import keyword
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Union

from dacite import from_dict

from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.item.item import Item
from my_dataclass.lol.item.item_combined import ItemCombined
from my_dataclass.lol.summoner_spell import SummonerSpell
from my_dataclass.lolapi.match.perk.perk import Perk
from my_dataclass.lolapi.match.role_lane import RoleLane
from my_dataclass.lolapi.match.team import Team
from my_dataclass.lolapi.match.team_info import TeamInfo
from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon
from my_dataclass.lolapi.summoner.summoner import Summoner
from util.dataclass_function import mapDataClassFields


@dataclass
class MatchParticipant:
    perk: Perk
    champion: Champion  # champion id -> Champion
    lane: RoleLane  # individualPosition +lane + role  + teamPosition  = lane -> Position / role
    summoner: Summoner  # summonerId summonerName -> Summoner
    summonerSpell1: SummonerSpell  # summoner1Id summonerId1 cast ->
    summonerSpell2: SummonerSpell  # summonerSpell2
    item0: Union[Item, ItemCombined, None]  # itemId -> Item
    item1: Union[Item, ItemCombined, None]
    item2: Union[Item, ItemCombined, None]
    item3: Union[Item, ItemCombined, None]
    item4: Union[Item, ItemCombined, None]
    item5: Union[Item, ItemCombined, None]
    item6: Union[Item, ItemCombined, None]
    team: TeamInfo
    assists: int = field(default=0)
    baronKills: int = field(default=0)
    bountyLevel: int = field(default=0)

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
    id: int = field(default=-1)
    pentaKills: int = field(default=0)
    physicalDamageDealt: int = field(default=0)
    physicalDamageDealtToChampions: int = field(default=0)
    physicalDamageTaken: int = field(default=0)
    quadraKills: int = field(default=0)
    riotIdName: str = field(default="")
    riotIdTagline: str = field(default="")
    sightWardsBoughtInGame: int = field(default=0)
    spell1Casts: int = field(default=0)
    spell2Casts: int = field(default=0)
    spell3Casts: int = field(default=0)
    spell4Casts: int = field(default=0)
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

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any], idx: int, team) -> "MatchParticipant":

        data['id'] = idx
        data['team'] = team.to_dict()

        data["summoner"] = {
            "puuid": data['puuid'],
            "id": data['summonerId'],
            "summonerLevel": data['summonerLevel'],
            "summonerName": data['summonerName'],
            "profileIconId":  dc.lol.profileIcons[str(data['profileIcon'])].to_dict()
        }
        champion = dc.lol.champions[data['championName']]
        champion.lvl = data['bountyLevel']
        champion.experience = data['champExperience']
        data['champion'] = champion.to_dict()
        data['lane'] = {
            "individualPosition": data['individualPosition'],
            "lane": data['lane'],
            "teamPosition": data['teamPosition'],
            "role": data['role'],
        }
        s1: SummonerSpell = dc.lol.getSummonerSpellById(data['summoner1Id'])
        s2: SummonerSpell = dc.lol.getSummonerSpellById(data['summoner2Id'])
        s1.casts = data['summoner1Casts']
        s2.casts = data['summoner2Casts']
        data['summonerSpell1'] = s1.to_dict()
        data['summonerSpell2'] = s2.to_dict()
        data['perk'] = Perk.from_dict(dc, data["perks"]).to_dict()
        data["item0"] = dc.lol.items[str(data['item0'])].to_dict() if data['item0'] != 0 else None
        data["item1"] = dc.lol.items[str(data['item1'])].to_dict() if data['item1'] != 0 else None
        data["item2"] = dc.lol.items[str(data['item2'])].to_dict() if data['item2'] != 0 else None
        data["item3"] = dc.lol.items[str(data['item3'])].to_dict() if data['item3'] != 0 else None
        data["item4"] = dc.lol.items[str(data['item4'])].to_dict() if data['item4'] != 0 else None
        data["item5"] = dc.lol.items[str(data['item5'])].to_dict() if data['item5'] != 0 else None
        data["item6"] = dc.lol.items[str(data['item6'])].to_dict() if data['item6'] != 0 else None

        data['nexusLost'] = data['nexusLost'] == 1
        data['nexusTakedowns'] = data['nexusTakedowns'] == 1

        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
