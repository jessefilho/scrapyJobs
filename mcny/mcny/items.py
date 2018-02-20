# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item,Field


class McnyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EventsItem(Item):
    organization = Field()
    description = Field()
    title = Field()
    ticketUrl = Field()
    eventWebsite = Field()
    street = Field()
    state = Field()
    zipCode = Field()
    last_updated = Field(serializer=str)