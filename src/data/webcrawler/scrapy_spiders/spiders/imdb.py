import os
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import ImdbItem
from dotenv import load_dotenv, find_dotenv

class SpiderIMDB(scrapy.Spider):
    name='imdb_com'

    start_urls = [
        # 'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&page=1&sort=boxoffice_gross_us,desc&ref_=adv_prv',
        # 'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&page=1&sort=moviemeter,asc&ref_=adv_prv',
        # 'http://www.imdb.com/search/title?genres=sci_fi&title_type=tv_series&sort=num_votes,desc&page=1&ref_=adv_prv',
        'http://www.imdb.com/search/title?genres=sci_fi&title_type=tv_series&page=1&sort=moviemeter,asc&ref_=adv_prv'
    ]

    # Find .env automagically by walking up directories until it's found
    # Load up the entries as environment variables
    load_dotenv(find_dotenv())
    RAW_DATA_PATH = os.environ.get("RAW_DATA_PATH")

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1,
                            'scrapy_spiders.pipelines.ImdbItemPipeline':300},
        'IMAGES_STORE': RAW_DATA_PATH+'/movies_imdb',
    }

    count_max = 4
    count = 1

    def parse(self, response):
        for title in response.css('div.lister-item-content'):
            # Follow link to movie detail page for poster, passing title and year data
            item = ImdbItem()
            href = 'http://www.imdb.com'+\
                title.css('h3.lister-item-header a::attr(href)').extract_first()
            item['title'] = title.css('h3.lister-item-header a::text').extract_first()
            item['year'] = title.css('span.lister-item-year::text').extract_first()
            request = scrapy.Request(href, callback=self.parse_cover)

            request.meta['item'] = item
            yield request

        # Stop following after count_max
        self.count += 1
        if self.count <= self.count_max:
            page_idx = response.url.find("page=")
            href = response.url.replace(
                        response.url[page_idx:page_idx+6], #doesn't work for double digits
                        'page='+str(self.count))

            yield response.follow(href, self.parse)

    def parse_cover(self, response):
        item = response.meta['item']
        item['image_urls'] = [response.xpath(\
                            '//div[contains(@class,"poster")]/a/img/@src'\
                            ).extract_first()]
        yield item
