import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from project_theassemblage.items import EventsItem
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
    allowed_domains = ["www.theassemblage.com/", "www.theassemblage.spaces.nexudus.com/"]
    start_urls = ["https://www.theassemblage.com/events.html",]
    
    

    def parse(self, response):
    	print('main_url: '+response.url)

        iframe_url = response.xpath('/html/body/iframe/@src').extract()[0]  

        #for see iframe url from src
        print('#####')
        print('iframe_url: '+iframe_url)
        print('#####')

        item = EventsItem()
        item['In_group_id'] = " "

        #getting url from src iframe
        request = scrapy.Request(url=iframe_url,
        callback=self.parse_iFramePage,
        errback=self.errback_httpbin,
        dont_filter=True)
        request.meta['item'] = item

        yield request

    def parse_iFramePage(self,response):
    	    
        item = response.meta['item']

        #concat the real url to events page
    	trash,url_aux = str(response.xpath('//div[@class="events-list__box"]/h3/a/@href').extract()[0]).split("events")
        url = 'https://theassemblage.spaces.nexudus.com/en/events' + url_aux

        #getting fields from events page
        item['title'] = response.xpath('//div[@class="events-list__box"]/h3/a/text()').extract()[0]
        item['organization'] = response.xpath('//div[@class="site-footer__section"]/ul/li/text()').extract()[0]
        item['street'] =response.xpath('//div[@class="site-footer__section"]/ul/li/text()').extract()[1]
        item['contactEmail'] = response.xpath('//div[@class="site-footer__section"]/ul/li/a/text()').extract()[0]
        city_aux, state_n_zipcode_aux = response.xpath('//div[@class="site-footer__section"]/ul/li/text()').extract()[2].split(",")
        item['city'] = city_aux
        
        remove_blankspace,item['state'],item['zipCode'] = state_n_zipcode_aux.split(" ")
        item['dateFrom'] = response.xpath('//div[@class="events-list__time"]/div/text()').extract()[0]
        item['eventWebsite'] =url
    	
        print('#####')
        print('event_url: '+url)
        print('#####')
        
        
        #into real event page
        request = scrapy.Request(url=url,
        callback=self.parse_eventPage,
        errback=self.errback_httpbin,
        dont_filter=True)
        request.meta['item'] = item
        
    	
    	return request

    def parse_eventPage(self,response):
    	item = response.meta['item']
    	preMainURL = 'https://theassemblage.spaces.nexudus.com'
        item['eventFlink'] = response.xpath('//div[@class="row"]//ul/li/a/@href').extract()[0]
        img_url = response.xpath('//div[@class="article-content"]/img/@src').extract()[0]
        item['eventImage'] = preMainURL+img_url
        item['description'] = response.xpath('//div[@class="article-content"]/div/p/text()').extract()[0]
    	#getting ticket url
        ticketUrl= preMainURL + str(response.xpath('//div[@class="btn-toolbar btn-toolbar--block events-detail__actions"]/a/@href').extract()[0])
    	
        item['ticketUrl'] = ticketUrl
        print('#####')
        print('ticketUrl: '+ticketUrl)
        print('#####')
        #getting start and end time
        startTime, endTime= response.xpath('//div[@class="events-detail__when"]//time/text()').extract()[0].split("-")
        item['endTime'] = endTime.strip()
        item['startTime'] = startTime.strip()
    	


    	#into ticket page
        request = scrapy.Request(url=ticketUrl,
        callback=self.parse_ticketPAge,
        errback=self.errback_httpbin,
        dont_filter=True)
        request.meta['item'] = item

    	return request

    def parse_ticketPAge(self, response):
        item = response.meta['item']
        #geolocation of event
        item['location'] = response.xpath('//div[@class="purchase-detail__where"]//a/@href').extract()[0]
        
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

	        	