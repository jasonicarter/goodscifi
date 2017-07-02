import os
import scrapy
from scrapy_spiders.pipelines import clean_title
from dotenv import load_dotenv, find_dotenv

class SpiderISFDB(scrapy.Spider):
    name='isfdb_com'

    start_urls = [
        'http://www.isfdb.org/cgi-bin/most_popular.cgi?1+all'
    ]

    # Find .env automagically by walking up directories until it's found
    # Load up the entries as environment variables
    load_dotenv(find_dotenv())
    RAW_DATA_PATH = os.environ.get("RAW_DATA_PATH")

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1},
        'IMAGES_STORE': RAW_DATA_PATH+'/books_isfdb'
    }

    def parse(self, response):
        for title in response.xpath('//table[contains(@class,"seriesgrid")]/tr'):
            # Follow link to book cover page passing title and year data
            if title.css('td::text') != []:
                href = title.css('td a::attr(href)').extract_first().replace('title', 'titlecovers')
                request = scrapy.Request(href, callback=self.parse_cover)
                request.meta['title'] = clean_title(title.css('td a::text').extract_first())
                request.meta['year'] = title.css('td::text')[2].extract()
                yield request


    def parse_cover(self, response):
        yield {
            'title': response.meta['title'],
            'year': response.meta['year'],
            # replace 'covers_md' with 'covers'
            'image_urls': [
                response.xpath(\
                '//div[contains(@id,"main")]/a/img/@src'\
                ).extract_first()]
        }
