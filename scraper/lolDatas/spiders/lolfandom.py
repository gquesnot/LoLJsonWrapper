import scrapy
from scrapy import Request

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.itemsName = kwargs.get('itemsName')

    def parse(self, response, **kwargs):

        for itemName in getattr(self, 'itemsName'):
            yield Request(url="http://leagueoflegends.fandom.com/wiki/" + itemName, callback=self.parse_item)

    def parse_item(self, response):
        item = Item()
        item["name"] = response.request.url.split('/')[-1].replace("_", " ")
        for attr in itemAttr:
            resp = response.xpath(XPATHS_ITEM[attr]).extract_first()

            item[attr] = resp if resp is None else int(resp.replace('+', "").replace("%", "").replace(" ", ""))

        yield item
