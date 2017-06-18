import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.pipelines import clean_title

class SpiderRT(scrapy.Spider):
    name='generic_com'

    # To be used for simple 1 page scraping
    start_urls = [
        # 'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=1',
        # 'http://www.ranker.com/crowdranked-list/the-greatest-sci-fi-movies?page=2'
        # 'http://scifilists.sffjazz.com/lists_film.html',
        # 'http://scifilists.sffjazz.com/lists_tv.html',
        'http://scifilists.sffjazz.com/lists_books_rank1.html'
    ]

    def parse(self, response):
        # ranker.com
        # for title in response.css('h2.listItem__h2'):
        #     yield {
        #         'title': clean_title(
        #             title.css('div.listItem__data a.listItem__title::text').extract_first()
        #             ),
        #         'year': None
        #     }

        # scifilists.sffjazz.com
        for title in response.css('div.dfltc tr'):
            yield {
                'title': clean_title(title.css('a::text').extract_first()),
                'year': title.css('td::text')[3].extract()
            }
