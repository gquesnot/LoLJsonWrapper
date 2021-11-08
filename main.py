from scrapy.crawler import CrawlerProcess

from lolClass.data_class.loldatacontroller import LolDataController

if __name__ == '__main__':
    dc = LolDataController(update=False, forceUpdate=True)
    for itemId, item in dc.itemsCombined.items():
        print(f"{itemId}: \n"
              f"    {item}"
              )
