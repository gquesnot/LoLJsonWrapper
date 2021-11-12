import keyword
from dataclasses import dataclass, asdict
from typing import Any, Dict, Union

from dacite import from_dict

from my_dataclass.lolapi.summoner.profile_icon import ProfileIcon


@dataclass
class Summoner:

    id: Union[str, None]
    accountId: Union[str, None]
    puuid: Union[str, None]
    name: Union[str, None]
    profileIcon: Union[ProfileIcon, None]
    revisionDate: Union[int, None]
    level: Union[int, None]

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Summoner":
        if "profileIconId" in data.keys():
            data['profileIcon'] = dc.lol.profileIcons[str(data['profileIconId'])].to_dict()
        data['level'] = data['summonerLevel']
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
