import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import RottenTmItem

class SpiderRT(scrapy.Spider):
    name='rotten_tomatoes_com'

    start_urls = [
        'https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/',
        ]

    def parse(self, response):
        # Only 1 page with 100 items to parse
        # Hidden elements causes some issue need to trim - postprocessing
        for title in response.css('div.content_body tr a'):
            item = RottenTmItem()
            # title and year in 'title' text
            item['title'] = title.css('::text').extract_first()
            item['year'] = title.css('::text').extract_first()
            yield item
