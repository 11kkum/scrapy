import scrapy
from world_jym.items import WorldJymItem

class WorldSpider(scrapy.Spider):
    name = 'world'
    allowed_domains = ['https://www.worldplus-gym.com']
    start_urls = ['https://www.worldplus-gym.com/shop/']

    def parse(self, response):
        item = WorldJymItem()
        store_links = response.css('div.shops-search-result a.link::attr(href)').getall()
        # item['store_name'] = response.css('div.shops-search-result h2::text').getall()

        for store_link in store_links:
            store_link = response.urljoin(store_link)
            request = scrapy.Request(url=store_link, callback=self.parse_store_page)
            request.meta['item'] = item  # Requestのmetaにitemを格納しておく。そしたらメソッド間で受け渡し可能 
            yield request

    def parse_store_page(self, response):
        item = response.meta['item']
        item['store_url'] = response.urljoin(response.url)
        item['store_name'] = response.css('div#shop-detail img').xpath("@alt").get()
        
        return item

