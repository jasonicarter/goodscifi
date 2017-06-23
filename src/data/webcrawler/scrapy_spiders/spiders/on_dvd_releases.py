import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import OnDvdItem

class SpiderOnDVD(scrapy.Spider):
    name='on_dvd_releases_com'

    start_urls = [
        'https://www.ondvdreleases.com/best-sci-fi-movies/page/1'
    ]

    page_limit = 20

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.OnDvdItemPipeline':300}
    }

    def parse(self, response):
        # sum_desc (overall rating)
        # gross_desc (theatrical gross (word wide))
        return scrapy.FormRequest.from_response(
            response,
            formid='sort_form',
            formdata={'order': 'sum_desc'},
            callback=self.page_sorted
        )

    def page_sorted(self, response):
        # 5 results per page
        for title in response.css('div.detailmainshort'):
            item = OnDvdItem()
            item['title'] = title.css('div.mtitle a::text').extract_first()
            item['year'] = title.css('div.mgenre::text').extract_first()
            yield item

        #Stop parsing if page limit is reached
        self.enforce_page_limit(response)

        # Follow pagination links
        # href pages appear as 1,2,3,4...32 so needed to do something different
        for page_no in range(2, self.page_limit+1):
            next_page = self.start_urls[0][:-1]+str(page_no)
            yield response.follow(next_page, self.page_sorted)

    def enforce_page_limit(self, response):
        current_page = response.css('div.top2 span.buttonsel::text').extract_first()
        if current_page == self.page_limit:
            raise CloseSpider('Reached requested page limit')
