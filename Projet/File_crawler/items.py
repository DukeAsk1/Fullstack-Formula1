# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    Date = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    Position = scrapy.Field()
    Number = scrapy.Field()
    Driver = scrapy.Field()
    Team = scrapy.Field()
    Laps = scrapy.Field()
    Lap_changed = scrapy.Field()
    Time = scrapy.Field()
    Points = scrapy.Field()
    Info = scrapy.Field()
    GP = scrapy.Field()
    Tyres = scrapy.Field()
    Num_stop = scrapy.Field()
    Q1 = scrapy.Field()
    Q2 = scrapy.Field()
    Q3 = scrapy.Field()
    Year = scrapy.Field()
    Avg_Speed = scrapy.Field()