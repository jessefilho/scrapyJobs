
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapyTest.items import EventsItem
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
    allowed_domains = ["mcny.org/"]
    start_urls = ["http://mcny.org/events/talks?page=0", "http://mcny.org/events/talks?page=1"]
    
    

    def parse(self, response):
    	print('main_url: '+response.url)
    	
    	eventLinks = response.xpath('.//div[@class="card-block"]//h2/a/@href').extract()
    	#str() to convert to string

        i = 0 #counter
        for linkForEachEvent in eventLinks:
        	item = EventsItem()
        	item['In_group_id'] = " "
        	item['eventFlink'] = response.xpath('//div[@class="social-set"]//li/a/@href').extract()[0]
        	item['eventTlink'] = response.xpath('//div[@class="social-set"]//li/a/@href').extract()[1]
        	item['eventIlink'] = response.xpath('//div[@class="social-set"]//li/a/@href').extract()[2]
        	item['organization'] = response.xpath("//meta[@property='og:site_name']/@content")[0].extract()
        	item['title']  = response.xpath('.//div[@class="card-block"]//h2/a/text()').extract()[i]
        	item['description']  = response.xpath('.//div[@class="card-block"]//div[@class="hidden-sm-down"]/text()').extract()[i]
        	url = "http://mcny.org" + linkForEachEvent
        	item['eventWebsite']  = str(url) #getting eventWebsite URL
        	#doing callback to the page of event
        	request = scrapy.Request(url=url,
    		callback=self.parse_EventPage,
    		errback=self.errback_httpbin,
    		dont_filter=True)
        	request.meta['item'] = item
        	


        	i = i + 1
        	yield request
        	

        

    def parse_EventPage(self,response):
    	item = response.meta['item']
    	url = str(response.xpath('.//*[@class="buy-tix"]//a/@href').extract()[0])
    	#getting datas
    	item['ticketUrl'] = url
    	item['eventImage'] = response.xpath('.//figure[@class="event-image"]/img/@src').extract()[0]
    	
    		
    	
    	#doing callback to the ticket page
    	request = scrapy.Request(url=url,
		callback=self.parse_TicketPage,
		errback=self.errback_httpbin,
		dont_filter=True)
    	request.meta['item'] = item

    	
    	return request

    def parse_TicketPage(self,response):
    	item = response.meta['item']
    	

    	#getting start and end time
    	item['startTime'] = response.xpath('.//*[@class="Programming_Event_StartTime"]/text()').extract()[0]
    	item['endTime'] = response.xpath('.//*[@class="Programming_Event_EndTime"]/text()').extract()[0]
    	#getting date from page ticket
    	datefrom_string = response.xpath('//h2[@class="Programming_Event_DateContainer"]/span/text()').extract()[0]
    	dayOfweed_aux,month_aux,day_aux = datefrom_string.split(" ")#split by blank space
    	item['dateFrom'] = datetime.strptime(month_aux[:3]+' '+day_aux+' 2017', '%b %d %Y').strftime("%d/%m/%Y")#I don't find the year, so here I suppose that the year is 2017
		#getting address data
    	adress_data = response.xpath('.//*[@class="MSFootTextDiv"]/p/a/text()').extract()[0]
    	street_aux,state_aux,zipCode_aux = adress_data.split(",")
    	item['street'] = str(street_aux)
    	item['state'] = str(state_aux)
    	item['zipCode'] = str(zipCode_aux)
    	#item['contactPhone'] = response.xpath('.//*[@class="MSFootTextDiv"]/p/span/text()').extract()[0]
    	item['eventPriceNonmembers'] = response.xpath('.//*[@class="Programming_Event_PriceList"]//span/text()').extract()[0]
    	item['eventPriceStudents'] = response.xpath('.//*[@class="Programming_Event_PriceList"]//span/text()').extract()[2]
    	item['eventPriceMembers'] = response.xpath('.//*[@class="Programming_Event_PriceList"]//span/text()').extract()[4]

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

	        	