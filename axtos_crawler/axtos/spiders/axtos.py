import scrapy
import re
from axtos.items import AxtosItem

class AxtosSpider(scrapy.Spider):
    name = 'axtos'
    allowed_domains = ['sc1.axtos.com']
    start_urls = ['http://sc1.axtos.com/shop']  #　店舗一覧ページ

    def parse(self, response):
        """"
        アコーディオンな表から各店舗個別のページのURLリストを作成
        そのリストに対してリクエストをかけて、parse_store_page関数を呼び出す
        """
        item = AxtosItem()
        #　store_linksは絶対パスで取得できる
        store_links = response.css('div.accordion2 h3 a::attr(href)').getall() # type : list
        # 各店舗にurlにリクエストを掛けて、parse_store_page関数を呼び出す

        for store_link in store_links:
            print(store_link)
            request = scrapy.Request(url = store_link, callback = self.parse_store_page)
            request.meta['item'] = item
            yield request

    
    def parse_store_page(self, response):
        """
        店舗情報のテーブルがあるクラスを取得して、項目とその内容を取得
        取得した項目とその内容をitem内にプッシュ
        各ジムのコース一覧情報が記載されているURLを取得して、
        そのURLにリクエストをかけparse_course_page関数を呼び出す
        """

        item = response.meta['item']
        item['store_name'] = response.css('div.ttl_bar h1::text').get().strip()
        item['store_url'] = response.url

        address_tmp = response.css('div.texts.text_link').xpath("string()").get().strip()
        item['address'] = address_tmp.split('\n')

        item['tel'] = response.css('div.texts.text_link a::attr(href)').get().strip()

        business_hours_tmp = response.css('ul.shop_data div.texts').xpath("string()")[1].get().strip()
        item['business_hours'] = re.sub(r'[\s]',"",business_hours_tmp)
        item['closed_days'] = response.css('ul.shop_data li.fix div.col div.texts p::text')[0].get()  
        item['parking_lot'] = response.css('ul.shop_data li.fix div.col div.texts p::text')[1].get() 


        item['facility'] = response.css('ul.facility_table li::text').getall()

        course_list_temp = response.css('ul.charge_list.table_mode h3::text').getall()
        option = response.css('ul.charge_list.table_mode.options h3::text').getall()
        item['option'] = option
        item['option_description'] = response.css('ul.charge_list.table_mode.options p.text::text').getall() 
        option_fee = response.css('ul.charge_list.table_mode.options p.text_em').xpath('string()').getall() 
        item['option_fee'] = option_fee
        # 差分をとって格納
        course_list = [i for i in course_list_temp if i not in option]
        item['course_list'] = course_list

        course_description_tmp = response.css('ul.charge_list.table_mode p.text::text').getall()
        price_table_text = response.css('ul.charge_list.table_mode.options p.text::text').getall()
        course_time = response.css('ul.charge_list.table_mode p.text.time::text').getall()
        course_target = response.css('ul.charge_list.table_mode p.text.target::text').getall() 
        price_table_text += course_time + course_target
        course_description = [i for i in course_description_tmp if i not in price_table_text]
        item['course_description'] = course_description
        item['course_time'] = course_time
        item['course_target'] = course_target 

        course_price_temp = response.css('ul.charge_list.table_mode p.text_em').xpath('string()').getall()
        course_price = [i for i in course_price_temp if i not in option_fee]
        item['course_price'] = course_price
        item['option_fee'] = option_fee
        
        item['initation'] = response.css('div.table_style dt').xpath('string()').getall()
        item['initation_fee'] = response.css('div.table_style dd').xpath('string()').getall()

        yield item