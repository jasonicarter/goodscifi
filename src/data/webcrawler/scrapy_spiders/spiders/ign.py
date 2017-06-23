import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import IgnItem

class SpiderIGN(scrapy.Spider):
    name='ign_com'

    start_urls = [
        'http://www.ign.com/lists/best-science-fiction-movies/1'
    ]

    page_limit = 100

    # Site blocks scrapy
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.IgnItemPipeline':300},
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):

        # 1 results per page
        for title in response.css('div.grid_16'):
            item = IgnItem()
            item['title'] = title.css('h1 a::text').extract_first()
            item['year'] = title.css('span::text').extract_first()
            yield item

        #Stop parsing if page limit is reached
        self.enforce_page_limit(response)

        # follow pagination links
        for href in response.css('div.topnitem_nextprev a::attr(href)'):
            yield response.follow(href, self.parse)

    def enforce_page_limit(self, response):
        current_page = response.xpath('//div[contains(@id,"topnitem_number")]/text()').extract_first()
        if int(current_page[1:]) == self.page_limit+1:
            raise CloseSpider('Reached requested page limit')
