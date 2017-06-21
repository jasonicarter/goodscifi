import scrapy
from scrapy_spiders.items import GenericItem

class SpiderWwendList(scrapy.Spider):
    name='wwe_lists_com'

    start_urls = [
        'https://www.worldswithoutend.com/lists_classics_of_sf.asp',
        'https://www.worldswithoutend.com/lists_sf_masterworks.asp',
        'https://www.worldswithoutend.com/lists_sf_mistressworks.asp',
        'https://www.worldswithoutend.com/lists_guardian_sff.asp',
        'https://www.worldswithoutend.com/lists_npr_sff.asp',
        'https://www.worldswithoutend.com/lists_pringle_sf.asp',
        'https://www.worldswithoutend.com/lists_sf101.asp',
        'https://www.worldswithoutend.com/lists_locus_bestsf.asp',
        'https://www.worldswithoutend.com/lists_EastonPress.asp',
        'https://www.worldswithoutend.com/lists_200SFBooksByWomen.asp',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_spiders.pipelines.GenericItemPipeline':300}
    }

    def parse(self, response):
        for title in response.xpath('//div[contains(@id,"reportlist")]/center/table/tr/td/table'):
            item = GenericItem()
            item['title'] = title.css('tr td p a::text').extract_first()
            item['year'] = title.css('tr td::text').extract_first()
            yield item
