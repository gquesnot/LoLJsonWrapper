from typing import Dict

from loldatacontroller import LolDataController
if __name__ == '__main__':
    dc = LolDataController(update=True, forceUpdate=False)
    dc.load(hint="lol", configs=["champions", "items", "itemsCombined"])

    for champName , champion in dc.champions.items():
        print(f"{champName}:", "\n    -".join([skin.name for skin in champion.skins]))

    for itemId , item in dc.items.items():
        print(item.id, item.name)

    for itemId, itemCombined, in dc.itemsCombined.items():
        print(itemCombined.id, itemCombined.name)
