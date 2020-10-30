# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AxtosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    store_name         = scrapy.Field() # 店舗名
    address            = scrapy.Field() # 住所
    tel                = scrapy.Field() # 電話番号
    business_hours     = scrapy.Field() # 営業時間
    closed_days        = scrapy.Field() # 休館日
    parking_lot        = scrapy.Field() # 駐車場
    course_list        = scrapy.Field() # コースリスト
    course_description = scrapy.Field() # コースの説明
    course_time        = scrapy.Field() # コースの利用可能時間・曜日
    course_target      = scrapy.Field() # コースの対象
    initation          = scrapy.Field() # 入会時に掛かる手数料
    initation_fee      = scrapy.Field() # 入会金
    course_price       = scrapy.Field() # 料金
    facility           = scrapy.Field() # 設備
    store_url          = scrapy.Field() # 店舗のURL 
    option             = scrapy.Field() # オプション
    option_description = scrapy.Field() # オプションの説明
    option_fee         = scrapy.Field() # オプションの料金