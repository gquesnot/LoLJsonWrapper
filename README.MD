## Keep Champions and Items from Lol up to date  and ready to use as dataclasses in python [see](https://docs.python.org/3/library/dataclasses.html)
#### I combined items from dragon data  with items from scraping on lol.fandom to get info i didn't find 

### Usage
Just init the LolDataController class and get your data

````python
from lolClass.data_class.loldatacontroller import LolDataController
from lolClass.data_class.item import Item
from new_data_class.item import Item as ItemCombined
from lolClass.data_class.champion import Champion

# optional parameter
# update       default = True      update if new version
# forceUpdate  default = False     force the update
ldc = LolDataController(update=True, forceUpdate=False)

# ATTRIBUTES
# raw items json data from dragon 
ldc.itemsJson

# raw items json data from scraping
ldc.itemsCrawlJson

# raw champion json data from dragon 
ldc.championsJson

# dict of items {itemId: Item}  from dragon json
ldc.items

# dict of combined items {itemId: ItemCombined} from dragon json and scraping
ldc.itemsCombined

# dict of champ {champName: Champion}
ldc.champions

````


### Install 
````shell
pip install -r requirements.txt
````


