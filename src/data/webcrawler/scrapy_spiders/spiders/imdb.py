import scrapy
from scrapy.exceptions import CloseSpider

class SpiderIMDB(scrapy.Spider):
    name='imdb_com'

    start_urls = [
        'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&page=1&sort=boxoffice_gross_us,desc&ref_=adv_prv',
    ]

    def parse(self, response):

        for item in response.css('div.lister-item-content'):
            yield {
                'title': item.css('h3.lister-item-header a::text').extract_first(),
                'year': item.css('span.lister-item-year::text').extract_first(),
            }

        # Stop parsing if page limit is reached
        self.enforce_page_limit(response)

        # follow pagination links
        for href in response.css('div.desc a::attr(href)'):
            yield response.follow(href, self.parse)

    def enforce_page_limit(self, response):
        if '&page=3&' in str(response.body):
            raise CloseSpider('reached requested page limit')
