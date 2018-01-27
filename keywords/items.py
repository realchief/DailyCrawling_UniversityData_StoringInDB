import scrapy
from scrapy.item import BaseItem
from collections import defaultdict


class KeywordsItem(scrapy.Item):

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()

        self._values[key] = value

    # create fields for items
    DOMAIN = scrapy.Field()
    FQDN = scrapy.Field()
    URL = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    hyperlinks = scrapy.Field()
    keywordInURL = scrapy.Field()
