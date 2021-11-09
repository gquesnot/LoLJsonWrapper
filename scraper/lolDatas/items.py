# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    hp = scrapy.Field()
    mana = scrapy.Field()
    mpregen = scrapy.Field()
    gold = scrapy.Field()
    hpregen = scrapy.Field()
    armor = scrapy.Field()
    ad = scrapy.Field()
    ap = scrapy.Field()
    mr = scrapy.Field()
    movespeed = scrapy.Field()
    movespeedpercent = scrapy.Field()
    attackspeedpercent = scrapy.Field()
    crit = scrapy.Field()
    lifestealpercent = scrapy.Field()
    omnivamppercent = scrapy.Field()
    armorpen = scrapy.Field()
    armorpenpercent = scrapy.Field()
    magicpenpercent = scrapy.Field()
    magicpen = scrapy.Field()
    ah = scrapy.Field()
    healshieldpower = scrapy.Field()
    name= scrapy.Field()

