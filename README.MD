## LoL Json Wrapper for Python

#### The goal of this project is to remove the complexity and boring stuff of using raw LOL / TFT json data.

- auto update Dragon Data on lol and tft on demand
- auto scrap missing items lol info
- load json datas as dataclasses [see](https://docs.python.org/3/library/dataclasses.html)
- parse api response to generate a better and more complete interface
- fast load with pickle


## LoL
### Data

- champions
- gameModes
- gameTypes
- items
- maps
- profileIcons
- queues
- seasons
- runes
- summonerSpells

### Api
- summoner
- match
- matchTimeline

## TFT
### data
- champions
- items
- traits


### Usage

look the [main_exemple.py](main_exemple.py) file

### Install

````shell
pip install -r requirements.txt
````

### TODO

- API dataclasses Interface to reformat json data from api in better way



