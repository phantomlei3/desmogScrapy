# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Webpage(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    citations = scrapy.Field()
    pass


class desmogOrgan(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    key_people = scrapy.Field()
    related_organs = scrapy.Field()
    pass