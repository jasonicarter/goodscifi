import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import GenericItem

class SpiderRT(scrapy.Spider):
    name='generic_com'

    # To be used for simple 1 page scraping
    start_urls = [
        # 'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=1',
        # 'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=2'
        # 'http://scifilists.sffjazz.com/lists_film.html',
        # 'http://scifilists.sffjazz.com/lists_tv.html',
        # 'http://scifilists.sffjazz.com/lists_books_rank1.html'
        'https://www.worldswithoutend.com/lists_classics_of_sf.asp'
    ]

    def parse(self, response):
        # ranker.com
        # for title in response.css('h2.listItem__h2'):
        #     item = GenericItem()
        #     item['title'] = title.css('div.listItem__data a.listItem__title::text').extract_first()
        #     item['year'] = None
        #     yield item

        # scifilists.sffjazz.com
        # for title in response.css('div.dfltc tr'):
        #     item = GenericItem()
        #     item['title'] = title.css('a::text').extract_first()
        #     item['year'] = title.css('td::text')[3].extract()
        #     yield item

        # world without end lists
        for title in response.xpath('//div[contains(@id,"reportlist")]/center/table/tr/td/table'):
            item = GenericItem()
            item['title'] = title.css('tr td p a::text').extract_first()
            item['year'] = title.css('tr td::text').extract_first()
            yield item
