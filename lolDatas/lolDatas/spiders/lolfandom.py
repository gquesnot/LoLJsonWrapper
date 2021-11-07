import scrapy
from scrapy import Request
from lolDatas.lolClass.data_class.datacontroller import DataController

from ..constants import XPATHS_ITEM
from ..items import Item

itemAttr = [
    "hp",
    "hpregen",
    "armor",
    "ad",
    "ap",
    "mr",
    "mpregen",
    "mana",
    "movespeed",
    "movespeedpercent",
    "attackspeedpercent",
    "crit",
    "lifestealpercent",
    "omnivamppercent",
    "armorpen",
    "armorpenpercent",
    "magicpenpercent",
    "magicpen",
    "ah",
    "healshieldpower"
]


class LolfandomSpider(scrapy.Spider):
    name = 'lolfandom'
    allowed_domains = ['leagueoflegends.fandom.com']
    start_urls = ['http://leagueoflegends.fandom.com/wiki/']

    def parse(self, response, **kwargs):
        items = DataController().getItemsNameAsUrl()
        for itemName in items:
            print(itemName)
            yield Request(url="http://leagueoflegends.fandom.com/wiki/" + itemName, callback=self.parse_item)

    def parse_item(self, response):
        item = Item()
        item["name"] = response.request.url.split('/')[-1].replace("_", " ")
        for attr in itemAttr:
            resp = response.xpath(XPATHS_ITEM[attr]).extract_first()

            item[attr] = resp if resp is None else resp.replace('+', "").replace("%", "").replace(" ", "")

        yield item
