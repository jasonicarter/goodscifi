import scrapy
from scrapy_spiders.items import GenericItem

class SpiderISFDB(scrapy.Spider):
    name='isfdb_com'

    start_urls = [
        'http://www.isfdb.org/cgi-bin/most_popular.cgi?1+all'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.GenericItemPipeline':300}
    }

    def parse(self, response):
        for title in response.xpath('//table[contains(@class,"seriesgrid")]/tr'):
            item = GenericItem()
            if title.css('td::text') != []:
                item['title'] = title.css('td a::text').extract_first()
                item['year'] = title.css('td::text')[2].extract()
                yield item
