# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_spiders.items import *
import re

# Need to deal with 's and : here and also in tmdb_posters
def clean_title(title):
    if title is None: return None

    title = title.strip() # Removing leading+trailing white space
    title = title.strip('[S1],[S2],[C]') # Books
    title = title.replace(' ', '-')
    return title

class ImdbItemPipeline(object):
    # Data issues to deal with
    # movie: {"title": "Jurassic World", "year": "(2015)"}
    # tv: {"title": "Jericho", "year": "(2006\u20132008)"}
    # tv: {"title": "Continuum", "year": "(I) (2012\u20132015)"}
    def process_item(self, item, spider):
        if isinstance(item, ImdbItem):
            if item['title']:
                item['title'] = clean_title(item['title'])
            if item['year']:
                item['year'] = re.sub('^\(.*\)\s|[()]|\u2013([0-9])*','',item['year'])
        return item

class OnDvdItemPipeline(object):
    # Data issues to deal with
    # "year": (2015 film) Action, Sci-Fi
    def process_item(self, item, spider):
        if isinstance(item, OnDvdItem):
            if item['title']:
                item['title'] = clean_title(item['title'])
            if item['year']:
                item['year'] = re.sub('[^0-9]*','',item['year'])
        return item

class RottenTmItemPipeline(object):
    # "year": \n            The Wizard of Oz (1939)
    # "year": Ghostbusters (1984 Original) (1984)
    def process_item(self, item, spider):
        if isinstance(item, RottenTmItem):
            if item['title']:
                # take everything from start to first (
                title = clean_title(item['title']).split('(')[0]
                year = item['title'][-6:].strip('()')
                item['title'] = title.rstrip('-')
            if item['year']:
                item['year'] = year
        return item

class IgnItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, IgnItem):
            if item['title']:
                item['title'] = clean_title(item['title'])
            if item['year']:
                item['year'] = item['year']
        return item

class GenericItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, GenericItem):
            if item['title']:
                item['title'] = clean_title(item['title'])
            if item['year']:
                item['year'] = re.sub('([0-9]*\.)|[^0-9]','',item['year'])
        return item
