import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.loader import ItemLoader

from project_acehotel.items import EventsItem
from datetime import datetime
from dateutil import parser
import json

import re


#from scrapy.item import Item, Field
#from scrapy.loader import ItemLoader



class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["acehotel.com/"]
    start_urls = ["https://www.acehotel.com/api/calendar/?hotel__slug=newyork&format=json"]
    
    

    def parse(self, response):
    	print('main_url: '+response.url)

        json_response = json.loads(response.body)
        for detailsAbout in json_response:
            item = EventsItem()
            item['In_group_id'] = " "
            item['organization'] = "ACE HOTEL"
            item['eventWebsite'] = "https://www.acehotel.com/calendar/"+detailsAbout['image_from_db']['section']+"/"+detailsAbout['slug']
            item['street'] = " 20 W 29th Street" #from contact page
            item['city'] = detailsAbout['hotel']['title']
            item['state'] = "NY" #from contact page
            item['zipCode'] = "10001" #from contact page
            
            item['title'] = detailsAbout['name']
            item['description'] = detailsAbout['event_description']
            item['eventImage'] = detailsAbout['image']
            item['dateFrom'] = datetime.strptime(detailsAbout['date'], '%Y-%m-%d').strftime('%d/%m/%Y') 

            dt_startTime = parser.parse(detailsAbout['start_datetime'])
            item['startTime'] = dt_startTime.strftime('%I:%M%p')

            dt_endTime = parser.parse(detailsAbout['end_datetime'])
            item['endTime'] = dt_endTime.strftime('%I:%M%p')

            item['eventTimeZone'] = detailsAbout['timezone']
            item['ticketUrl'] = detailsAbout['ticketing_url']
            item['contactEmail'] = detailsAbout['rsvp_email_replyto']
            item['location'] = detailsAbout['venue']['title']


            

            yield item
            


    	

        

    def parse_eventPage(self,response):
    	item = response.meta['item']
    	item['eventImage'] = response.xpath('//div[@class="slider"]//img/@src').extract()[0]
    	item['description'] = re.sub('[^A-Za-z0-9-. ]+', '',response.xpath('//div[@class="row description"]/div//p//text()').extract()[0])
    	
    	#Title try/except
    	try:
    		title1 = response.xpath('//*[@class="header"]//text()').extract()[0]
    		title2 = response.xpath('//*[@class="header"]//text()').extract()[1]
    		item['title'] =  title1 +" "+ title2 
    		
    	except IndexError as e:
    		
    		print(e)
    		item['title'] =  title1

    	#Date try/except
    	try:
    		data_aux = response.xpath('//h3[@class="subheader"]/text()').extract()[0]
    		day_aux, date_aux = data_aux.split(",")
    		month_aux, days_aux, year_aux = date_aux.split(".")
    		item['dateFrom'] = days_aux.strip()+"/"+month_aux.strip()+"/"+year_aux.strip()
    		
    		
    	except ValueError as e:
    		print(e)
    		item['dateFrom'] = "special date settings"

    	# time try/except
    	try:
    		time_aux = response.xpath('//h3[@class="subheader"]/text()').extract()[1]
    		time_aux = re.sub('[^A-Za-z0-9-: ]+', '', time_aux)
    		time_Start_aux, time_End_aux  = time_aux.split("-")
    		item['startTime'] = time_Start_aux.strip()
    		item['endTime'] = time_End_aux.strip()
    	except Exception as e:
    		print(e)
    		item['startTime'] = " "
    		item['endTime'] = " "


    	
    	
    	
    	

    	# Price group try/except
    	try:
    		pricesGroup = []
    		for pricesList in response.xpath('//div[@class="col-sm-3 tickets"]/p/text()').extract():
    			if pricesList.strip():
    				pricesGroup.append(pricesList) 

    		
    		item['eventPrice'] = pricesGroup[0]
    		
    		
    	except IndexError as e:
    		print(e)
    		item['eventPrice'] = " "
    		
    	try:
    		item['eventPriceMembers'] = pricesGroup[1]
    		
    	except IndexError:
    		item['eventPriceMembers'] = " "

    	try:
    		linkForEachTicketPage = response.xpath('//div[@class="row description"]/div[@class="col-sm-3"]/a/@href').extract()[0]
    		item['ticketUrl'] = linkForEachTicketPage

    		# request = scrapy.Request(url=linkForEachTicketPage,
      #   	callback=self.parse_ticketPage,
      #   	errback=self.errback_httpbin,
      #   	dont_filter=True)
      #   	request.meta['item'] = item

    		
    	except IndexError:
    		item['ticketUrl'] = " "

    	
    	
    	return item
    	
    def parse_ticketPage(self,response):
    	    
        item = response.meta['item']
        
    	
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

