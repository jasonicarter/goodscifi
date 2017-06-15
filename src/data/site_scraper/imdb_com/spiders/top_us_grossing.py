import scrapy

class TopUSGrossing(scrapy.Spider):
    name='top_grossing'

    start_urls = [
        'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&page=1&sort=boxoffice_gross_us,desc&ref_=adv_prv',
    ]
    
    def parse(self, response):
        for item in response.css('div.lister-item-content'):
            yield {
                'title': item.css('h3.lister-item-header a::text').extract_first(),
                'year': item.css('span.lister-item-year::text').extract_first(),
            }

        # follow pagination links
        for href in response.css('div.desc a::attr(href)'):
            yield response.follow(href, self.parse)
