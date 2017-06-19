import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.pipelines import clean_title

class SpiderWwEnd(scrapy.Spider):
    name='wwend_com'

    def start_requests(self):
        for year_published in range(2017,2018,1):
            yield scrapy.Request(\
            'https://www.worldswithoutend.com/lists_booksbyyear.asp?p=1&YearPublished=%s&Genre=SF&NovelType=1&Nominated='\
            % year_published)

    def parse(self, response):
        for title in response.xpath('//div[contains(@id,"reportlist")]/table/tr/td/table/td'):
            yield {
                'title': clean_title(title.css('table tr td p a::text').extract_first()),
                # Using url obtained from pagination - index should be okay to use
                'year': response.url[response.url.find('YearPublished=')+14:response.url.find('&Genre=')]
            }

        # follow pagination links
        for href in response.css('div.content a::attr(href)'):
            yield response.follow(href, self.parse)
