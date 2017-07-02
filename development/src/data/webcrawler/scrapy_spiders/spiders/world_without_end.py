import os
import scrapy
from scrapy_spiders.pipelines import clean_title
from dotenv import load_dotenv, find_dotenv

class SpiderWwEnd(scrapy.Spider):
    name='wwend_com'

    # Find .env automagically by walking up directories until it's found
    # Load up the entries as environment variables
    load_dotenv(find_dotenv())
    RAW_DATA_PATH = os.environ.get("RAW_DATA_PATH")

    # Used for downloading images
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1},
        'IMAGES_STORE': RAW_DATA_PATH+'/wwend_books',
        # 'CONCURRENT_REQUESTS': 1,
        # 'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for year_published in range(1930, 2018, 1):
            yield scrapy.Request(\
            'https://www.worldswithoutend.com/lists_booksbyyear.asp?p=1&YearPublished=%s&Genre=SF&NovelType=1&Nominated='\
            % year_published)

    def parse(self, response):
        for title in response.xpath('//div[contains(@id,"reportlist")]/table/tr/td/table/td'):
            if title.css('table tr div.awardslisting img') != []:
                yield {
                    'title': clean_title(title.css('table tr td p a::text').extract_first()),
                    # Using url obtained from pagination html - index should be okay
                    'year': response.url[
                        response.url.find('YearPublished=')+14:response.url.find('&Genre=')],
                        # replace 'covers_md' with 'covers'
                    'image_urls': ['https://www.worldswithoutend.com/'+\
                        title.css('table tr div.awardslisting img::attr(src)').extract_first().replace('covers_md', 'covers')]
                }

        # follow pagination links
        for href in response.css('div.content a::attr(href)'):
            yield response.follow(href, self.parse)
