# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


# class ProjectTheassemblageItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
    
class CarsItem(Item):
    #REQUIRED FIELDS
    brand = Field() 
    model = Field()
    exact_model = Field()
    price_second_hand = Field() 
    published = Field() #date that the post published
    updated = Field() #date that the post updated
    price_new = Field()
    year = Field()
    kilometers = Field()
    city = Field()
    gear = Field()
    doors = Field()

    seats = Field()
    cv = Field()
    combustible = Field()
    garantia = Field()  
    color = Field()
    altura = Field() 
    longitud = Field() 
    anchura = Field() 
    volumen maletero = Field()
    velocidad maxima = Field()
    urbano = Field()    
    extraurbano = Field()    
    mixto = Field()     
    peso = Field()
    deposito = Field()
    aceleracion = Field()
    



    last_updated = Field(serializer=str)
    pass