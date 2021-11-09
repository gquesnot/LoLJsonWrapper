from typing import Dict

from loldatacontroller import LolDataController

if __name__ == '__main__':
    # init function with his default parameter
    dc = LolDataController(update=True, forceUpdate=False)
    # loading function with his default parameters
    # update all data from lol + load all data or only some
    dc.load(hint="lol", configs=["champions", "items", "itemsCombined"])

    # champ from dragon json light and full
    for champName, champion in dc.champions.items():
        print(f"{champName}:", "\n    -".join([skin.name for skin in champion.skins]))

    # item from dragon json
    for itemId, item in dc.items.items():
        print(item.id, item.name)

    # items combined
    for itemId, itemCombined, in dc.itemsCombined.items():
        print(itemCombined.id, itemCombined.name)
