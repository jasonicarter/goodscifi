# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Need multiple items due to diff spider data clean up requirements
# See pipelines.py

class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class OnDvdItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()

class RottenTmItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()

class IgnItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()

class GenericItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
