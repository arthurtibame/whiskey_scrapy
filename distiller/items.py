# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DistillerItem(scrapy.Item):
    
    name = scrapy.Field() # 酒名    
    winery = scrapy.Field() # 酒廠       
    url = scrapy.Field() # URL
    abv = scrapy.Field() # 濃度
    year = scrapy.Field() # 年份
    origin = scrapy.Field() # 產地
    image = scrapy.Field() # 圖片
    official_content = scrapy.Field() # 官方內容
    
class DistillerCommentItem(scrapy.Item):
    
    name = scrapy.Field()  # 酒名
    star = scrapy.Field()  # 評分      
    comment = scrapy.Field() # 評論       