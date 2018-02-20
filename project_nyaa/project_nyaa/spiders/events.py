import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from project_nyaa.items import EventsItem
from scrapy.http import HtmlResponse
from scrapy import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.loader import ItemLoader

from datetime import datetime
import re



class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["nyaa.edu/"]
    start_urls = ["https://nyaa.edu/exhibitions-lectures/past-lectures/upcoming-lectures/"]
    
    

    def parse(self, response):
        print('main_url: '+response.url)

        eventLinks = response.xpath('.//div[@class="lectures-excerpt-image"]/div[@class="excerpt-image-right"]/a/@href').extract()
        #str() to convert to string

        i = 0 #counter
        for linkForEachEvent in eventLinks:
            item = EventsItem()
            item['In_group_id'] = " "
            item['organization'] ="New York Academy of Art"
            item['title']  = response.xpath('.//div[@class="lectures-excerpt-image"]/div[@class="excerpt-image-right"]/h3/text()').extract()[i]
            item['eventImage'] = response.xpath('.//div[@class="lectures-excerpt-image"]/div[@class="lectures-excerpt-image-left"]/img/@src').extract()[i]
            dateEvent_aux = response.xpath('//div[@class="lectures-excerpt-image"]/div[@class="excerpt-image-right"]/p/text()').extract()[i]
            day_aux, month_auxDay, hour_aux  = dateEvent_aux.split(',')
            item['startTime'] = hour_aux.strip()
            
            #extract date
            month_auxDay = month_auxDay.strip()
            month_aux,day_aux = month_auxDay.split(" ")
            item['dateFrom'] = datetime.strptime(month_aux[:3]+' '+day_aux+' 2018', '%b %d %Y').strftime("%d/%m/%Y")#I don't find the year, so here I suppose that the year is 2018

            item['eventWebsite'] = linkForEachEvent

            street_aux, city_aux = response.xpath('.//p[@class="right"]/text()').extract()[0].split('|')
            item['street'] = street_aux.strip()
            city_aux, state_aux = city_aux.split(",")
            item['city'] = city_aux.strip()
            state_aux = state_aux.strip()
            state_aux,zipCode_aux = state_aux.split(" ")

            item['state'] = state_aux.strip()
            item['zipCode'] = zipCode_aux.strip()

            #not found url to ticket page
            item['ticketUrl'] = " "
            #social links
            item['eventFlink'] = response.xpath('.//div[@id="social-icons"]/a/@href').extract()[0]
            item['eventTlink'] = response.xpath('.//div[@id="social-icons"]/a/@href').extract()[1]
            item['eventIlink'] = response.xpath('.//div[@id="social-icons"]/a/@href').extract()[2]
            #contact from footer
            item['contactEmail'] = "inquiries@nyaa.edu"
            

            
            
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
        item['description'] = response.xpath('.//div[@class="entry"]/p/text()').extract()[0][:200]
        
        
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

                