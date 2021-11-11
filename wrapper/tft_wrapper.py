import zipfile
from typing import Dict
from urllib.request import urlretrieve

from my_dataclass.tft.champion.champion import Champion
from my_dataclass.tft.item.item import Item
from my_dataclass.tft.trait.trait import Trait
from my_dataenum.config_index import ConfigIndex
from util.base_wrapper import BaseWrapper


class TftWrapper(BaseWrapper):
    hint = "tft"

    configsDict = [
        {
            "name": "traits",
            "class_": Trait,
            "configIndex": ConfigIndex.ID

        },
        {
            "name": "champions",
            "class_": Champion,

        },
        {
            "name": "items",
            "class_": Item,
            "configIndex": ConfigIndex.ID
        }

    ]

    jsonDownloadUrl = "https://static.developer.riotgames.com/docs/tft/set5patch1115.zip"

    champions: Dict[str, Champion]
    items: Dict[str, Item]
    traits: Dict[str, Trait]

    def __init__(self, dc):
        super().__init__(dc)
        path = self.getPath("data.zip")

    def loadChampions(self):
        config = self.getConfigByName("champions")
        traits = self.getDatas("traits")
        for champ in config.json:
            myTraits = [traits[trait] for trait in champ['traits']]
            champion = config.class_.from_dict(champ, myTraits)
            config.addData(champion.name, champion)
        return config

    def downloadJson(self):
        if self.dc.showLog:
            print("downloading json tft ... ", end="")
        filehandle, _ = urlretrieve(self.jsonDownloadUrl)
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        for file in zip_file_object.namelist():
            configName = file.replace(".json", "")
            if configName in self.allConfig:
                jsonData = zip_file_object.open(file).read().decode("utf-8")
                config = self.getConfigByName(configName)
                with open(self.getPath(f"{config.path}.json"), "w+") as f:
                    f.write(jsonData)
        if self.dc.showLog:
            print("done")
