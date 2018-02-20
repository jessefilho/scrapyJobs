import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from project_npg.items import EventsItem
from scrapy.http import HtmlResponse
from scrapy import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from datetime import datetime


#from scrapy.item import Item, Field
#from scrapy.loader import ItemLoader



class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["npg.si.edu/"]
    start_urls = ["http://npg.si.edu/whats-on/events"]
    
    

    def parse(self, response):
    	print('main_url: '+response.url)

        eventLinks = response.xpath('.//div[@class="moth-event"]//div[@class="event-content"]/h4/a/@href').extract()
        #str() to convert to string

        i = 0 #counter
        for linkForEachEvent in eventLinks:
            item = EventsItem()
            item['In_group_id'] = " "
            item['title']  = response.xpath('.//div[@class="moth-event"]//div[@class="event-content"]/h4/a/text()').extract()[i]
            item['eventWebsite'] = linkForEachEvent
            
            #getting date from page ticket
            month_aux = response.xpath('.//div[@class="date-wrapper"]//span[@class="month"]/text()').extract()[i].strip()
            day_aux = response.xpath('.//div[@class="date-wrapper"]//span[@class="numeric-day"]/text()').extract()[i].strip()

            item['dateFrom'] = datetime.strptime(month_aux[:3]+' '+day_aux+' 2018', '%b %d %Y').strftime("%d/%m/%Y")#I don't find the year, so here I suppose that the year is 2018


            #automation of ticket button available 
            try:
                item['ticketUrl'] = response.xpath('//div[@class="event-content"]/a[@class="btn accent"]/@href').extract()[i]
            except IndexError:
                item['ticketUrl'] = " "
            
            #catching exception os unpack values at split by ","
            try:
                item['city'],item['state'] = response.xpath('//p[@class="location"]/text()').extract()[i].split(",")
            except ValueError:
                item['city'] = "Washington"
                item['state'] = "DC"
            
            #callback to event page
            request = scrapy.Request(url=linkForEachEvent,
            callback=self.parse_eventPage,
            errback=self.errback_httpbin,
            dont_filter=True)
            request.meta['item'] = item


            i = i + 1
            yield request

    def parse_eventPage(self,response):
    	    
        item = response.meta['item']
        item['organization'] = response.xpath('.//div[@class="venue-detail"]/h3/text()').extract()[0]
        item['street'] = response.xpath('.//div[@class="venue-detail"]/p/text()').extract()[0]

        #Cracking link from Gmaps to extracting the zip code
        
        list_TocrackLink = []

        try:
            
            list_TocrackLink = response.xpath('.//div[@class="venue-detail"]/p/a/@href').extract()[0].split(",")
            list_TocrackLink = list_TocrackLink[2].split("/")
            list_TocrackLink = list_TocrackLink[0].split("+")
            item["zipCode"] = list_TocrackLink[2] #extracting from googleMap link the zipCode
        except IndexError:
            list_TocrackLink = response.xpath('//div[@class="venue-detail"]/p/text()').extract()[0].split(",")
            list_TocrackLink = list_TocrackLink[2].split(" ")
            item["zipCode"] = list_TocrackLink[2]

        
        
        item['startTime'] = response.xpath('.//p[@class="event-time"]/strong/text()').extract()[0]
        
        #there one exeception that crash it
        try:
            item['endTime'] = response.xpath('.//p[@class="event-time"]/strong/text()').extract()[1]
        except IndexError:
            item['endTime'] = " "
        
        item['description'] = response.xpath('//div[@class="event-description"]/p/text()').extract()[0]
        
        
        
    	
    	return item

    #catch exceptions in request processing	
    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

	        	