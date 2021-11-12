from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, Union

from dacite import from_dict

from my_dataclass.gold import Gold
from my_dataclass.image import Image
from my_dataclass.lol.champion.champion import Champion
from my_dataclass.lol.item.item_stats import ItemStats


@dataclass
class ItemCombined:
    id: int
    name: str
    description: str
    colloq: str
    plaintext: str

    image: Image
    gold: Gold
    tags: List[str]
    stats: ItemStats
    maps: List[int]
    specialRecipe: Union[int, None] = field(default=None)
    stacks: int = field(default=0)
    depth: int = field(default=0)
    from_: Union[None, List[str]] = field(default=None)
    into: Union[None, List[str]] = field(default=None)
    consumed: bool = field(default=False)
    consumeOnFull: bool = field(default=False)

    requiredChampion: Union[Champion, None] = field(default=None)
    inStore: bool = field(default=True)
    hideFromAll: bool = field(default=False)

    @classmethod
    def from_dict(cls, itemId: int, champions: Dict[str, Champion], crawlItem: Dict[str, Any],
                  dataItem: Dict[str, Any]) -> "ItemCombined":
        dataItem['id'] = int(itemId)
        dataItem['stats'] = {k: v for k, v in crawlItem.items() if k != "name"}
        for k, v in dataItem['stats'].items():
            if "percent" in k and v is not None:
                dataItem['stats'][k] = round(v / 100, 2)
        if "requiredChampion" in dataItem.keys():
            champName = dataItem["requiredChampion"]
            champion = None
            if champName not in champions.keys():

                if champName.capitalize() not in champions.keys():
                    print("ERRROR")
                else:
                    champion = champions[champName.capitalize()]
            else:
                champion = champions[champName]

            dataItem["requiredChampion"] = champion
        if "specialRecipe" in dataItem.keys():
            dataItem["specialRecipe"] = int(dataItem['specialRecipe'])

        dataItem['maps'] = [int(mapId) for mapId, v in dataItem['maps'].items() if v]
        return from_dict(cls, data=dataItem)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
