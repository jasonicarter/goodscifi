import scrapy
from scrapy_spiders.items import GenericItem

class SpiderGoodReads(scrapy.Spider):
    name='goodreads_com'

    start_urls = [
        'https://www.goodreads.com/list/show/4893.Best_Science_Fiction_of_the_21st_Century?page=1',
        'https://www.goodreads.com/list/show/4893.Best_Science_Fiction_of_the_21st_Century?page=2',
        'https://www.goodreads.com/list/show/35776.Most_Popular_Science_Fiction_on_goodreads_with_over_50_thousand_ratings?page=1',
        'https://www.goodreads.com/list/show/35776.Most_Popular_Science_Fiction_on_goodreads_with_over_50_thousand_ratings?page=2',
        'https://www.goodreads.com/list/show/19341.Best_Science_Fiction?page=1',
        'https://www.goodreads.com/list/show/19341.Best_Science_Fiction?page=2',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.GenericItemPipeline':300}
    }

    def parse(self, response):
        for title in response.xpath('//div[contains(@id,"all_votes")]/table/tr'):
            item = GenericItem()
            item['title'] = title.css('td a.bookTitle span::text').extract_first()
            item['year'] = None
            yield item
