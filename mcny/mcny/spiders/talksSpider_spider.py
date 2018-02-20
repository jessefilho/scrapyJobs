
import scrapy
from events.items import EventsItem

from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import Request
import urllib
from scrapy.selector import HtmlXPathSelector


#from scrapy.item import Item, Field
#from scrapy.loader import ItemLoader



class TalksSpider(scrapy.Spider):
    name = "talksSpider"
    allowed_domains = ["mcny.org/"]
    start_urls = ["http://mcny.org/events/talks?page=0", "http://mcny.org/events/talks?page=1"]

    def parse(self, response):
    	items = EventsItem()

    	organization =[]
    	title_eventsObj =[]
    	descriptionsObj =[]
    	eventWebsitesObj =[]
    	ticketUrl = []
    	street = []
    	state = []
    	zipCode = []
    	startTime = []
    	endTime = []
    	eventPriceLabel = []
    	eventPriceDollar = []
    	eventPriceList = []	
    	imageURL = []
    	contactPhone = []
    	
        for talksPage in response.css('section.events-all'):

        	
        	
        	test['title']  = talksPage.xpath('.//div[@class="card-block"]//h2/a/text()').extract()
        	test['description']  = talksPage.xpath('.//div[@class="card-block"]//div[@class="hidden-sm-down"]/text()').extract()
        	test['eventWebsite']  = "http://mcny.org" + talksPage.xpath('.//div[@class="card-block"]//h2/a/@href').extract()
        	

        	yield test
        	
	        	