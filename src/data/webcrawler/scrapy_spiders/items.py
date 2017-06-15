# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapySpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()