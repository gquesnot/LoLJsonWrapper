## Combine dragondata item and champion with scrapping on lol.fandom to get them as data_class


###Usage
Just init the LolDataController class and get your data

````python
from lolClass.data_class.loldatacontroller import LolDataController
from lolClass.data_class.item import Item
from new_data_class.item import Item as ItemCombined
from lolClass.data_class.champion import Champion

# optional parameter
# update=True : update if new version
# forceUpdate=False : force the update
ldc = LolDataController()

# ATTRIBUTES
# raw items dragon json data 
ldc.itemsJson

# raw items scrapping json data
ldc.itemsCrawlJson

# raw champion dragon json data
ldc.championsJson

# dict of items {itemId: Item}  from dragon json
ldc.items

# dict of combined items {itemId: ItemCombined} from dragon json and scraping
ldc.itemsCombined

# dict of champ {champName: Champion}
ldc.champions

````


### Install 
````
pip install -r requirements.txt
````


