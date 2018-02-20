import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from project_madmuseum.items import EventsItem
from scrapy.http import HtmlResponse
from scrapy import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.loader import ItemLoader

from datetime import datetime
from dateutil.parser import parse
import re



class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["madmuseum.org/","https://www.eventbrite.com/"]
    start_urls = ["http://madmuseum.org/calendar?d=2018-02"]
    
    

    def parse(self, response):
        print('main_url: '+response.url)

        eventLinks = response.xpath('.//div[@class="event-listing-image"]//a/@href').extract()
        

        i = 0 #counter
        
        for linkForEachEvent in eventLinks:
            item = EventsItem()
            item['In_group_id'] = " "
            item['description'] = response.xpath('.//div[@class="listings-summary"]/p/text()').extract()[i]
            item['organization'] ="the museum of arts and design"
            item['eventImage'] = response.xpath(".//div[@class='event-listing-image']/a/img/@src").extract()[i]
            
            
            
            #extract date
            try:
                dateFrom_aux = response.xpath(".//div[@class='listings-starttime']/span[@class='date-display-single']/span[@class='date-display-range']/span[@class='date-display-start']/@content").extract()[i]
                dt = parse(dateFrom_aux)
                item['dateFrom'] = dt.strftime('%d/%m/%Y')

            except IndexError:
                item['dateFrom'] = " "
            
            #tag html for starttime without span tag, it cause exceptions for extract some cases.
            try:
                item['startTime'] = response.xpath(".//div[@class='listings-starttime']/span[@class='date-display-single']/span[@class='date-display-range']/span[@class='date-display-start']/text()").extract()[i]
            except IndexError:
                item['startTime'] = " "
          
            try:
                item['endTime'] = response.xpath(".//div[@class='listings-starttime']/span[@class='date-display-single']/span[@class='date-display-range']/span[@class='date-display-end']/text()").extract()[i]
            except IndexError:
                item['endTime'] = " "
            

            linkForEachEvent = "http://madmuseum.org" + linkForEachEvent
            item['eventWebsite'] = linkForEachEvent
            item['street'] = "2 COLUMBUS CIRCLE"
            item['city'] = "New York"
            item['state'] = "NY"
            item['zipCode'] = "10019"

            
            #social links
            item['eventFlink'] = response.xpath('.//div[@id="social"]//li//@href').extract()[0]
            item['eventTlink'] = response.xpath('.//div[@id="social"]//li//@href').extract()[2]
            item['eventIlink'] = response.xpath('.//div[@id="social"]//li//@href').extract()[1]
            
            
            

            
            
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
        item['title'] = re.sub('[^A-Za-z0-9-. |]+', '',response.xpath('.//div[@id="page_title"]/text()').extract()[0])
        #try getting room if there.
        try:
            item['room'] = re.sub('[^A-Za-z0-9-. ]+', '',response.xpath(".//div[@class='event_location_field']/text()").extract()[0])
        except IndexError:
            item['room'] = " "

        
        try:
            ticketUrl_aux = response.xpath(".//div[@class='event_purchase_field']/a/@href").extract()[0]
            
            if ticketUrl_aux.find("mailto") == 0:
                ticketUrl_aux = " "

            
            
           
            #callback to ticket page
            request = scrapy.Request(url=ticketUrl_aux,
                callback=self.parse_ticketPage,
                errback=self.errback_httpbin,
                dont_filter=True)
            request.meta['item'] = item
        except ValueError:
            item['ticketUrl'] = " "
            return item
        except IndexError:
            item['ticketUrl'] = " "
            return item
        

        return request

    def parse_ticketPage(self,response):
        item = response.meta['item']
        
        item['ticketUrl'] = response.url
        item['eventPrice'] = response.xpath(".//div[@class='js-display-price']/text()").extract()[0]

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

                