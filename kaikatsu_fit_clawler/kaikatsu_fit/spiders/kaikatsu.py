import scrapy


class KaikatsuSpider(scrapy.Spider):
    name = 'kaikatsu'
    allowed_domains = ['fit24.jp']
    start_urls = ['http://fit24.jp/shop_result.html']

    def parse(self, response):
        pass
