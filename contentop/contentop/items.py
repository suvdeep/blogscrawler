# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentopItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    statuscode = scrapy.Field()
    #crawled = scrapy.Field()
    pass


# http://www.adverblog.com

# /html/body/div[2]/div[3]/div[1]/h1

# /html/body/div[2]/div[3]/div[1]//p/text()