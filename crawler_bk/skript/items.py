# -*- coding: utf-8 -*-

import scrapy


class Event(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    pricing_min = scrapy.Field()
    pricing_max = scrapy.Field()
    pricing_currency = scrapy.Field()
    address = scrapy.Field()
    label = scrapy.Field()
    timestamp = scrapy.Field()
