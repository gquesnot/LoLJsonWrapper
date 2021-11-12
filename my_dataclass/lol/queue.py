from dataclasses import dataclass, asdict
from typing import Any, Union, Dict

from dacite import from_dict

from my_dataclass.lol.map import Map


@dataclass
class Queue:
    id: int
    map: Union[str, Map]
    description: Union[None, str]
    notes: Union[None, str]

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "Queue":
        data['id'] = data['queueId']
        myMap = None
        for mapId, map_ in dc.lol.maps.items():
            if map_.name == data['map']:
                myMap = map_
        if myMap is not None:
            data['map'] = myMap.to_dict()
        # data = {k if k in keyword.kwlist else k + "_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
