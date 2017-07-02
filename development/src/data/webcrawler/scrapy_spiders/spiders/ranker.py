import scrapy
from scrapy_spiders.items import GenericItem

class SpiderRanker(scrapy.Spider):
    name='ranker_com'

    start_urls = [
        'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=1',
        'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=2'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.GenericItemPipeline':300}
    }

    def parse(self, response):
        for title in response.css('h2.listItem__h2'):
            item = GenericItem()
            item['title'] = title.css('div.listItem__data a.listItem__title::text').extract_first()
            item['year'] = None
            yield item
