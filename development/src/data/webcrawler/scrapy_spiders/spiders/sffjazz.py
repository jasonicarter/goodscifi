import scrapy
from scrapy_spiders.items import GenericItem

class SpiderSFF(scrapy.Spider):
    name='sff_com'

    start_urls = [
        'http://scifilists.sffjazz.com/lists_film.html',
        'http://scifilists.sffjazz.com/lists_tv.html'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.GenericItemPipeline':300}
    }

    def parse(self, response):
        for title in response.css('div.dfltc tr'):
            item = GenericItem()
            item['title'] = title.css('a::text').extract_first()
            if 'lists_tv' in response.url:
                item['year'] = title.css('td::text')[2].extract()
            else:
                item['year'] = title.css('td::text')[3].extract()
            yield item
