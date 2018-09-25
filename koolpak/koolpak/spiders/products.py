import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from koolpak.items import ProductsItem
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
import unicodedata



class EventsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["koolpak.com/"]
    start_urls = ["http://koolpak.com/shop/page/1/",
    "http://koolpak.com/shop/page/2/",
    "http://koolpak.com/shop/page/3/",
    "http://koolpak.com/shop/page/4/",
    "http://koolpak.com/shop/page/5/",
    "http://koolpak.com/shop/page/6/",
    "http://koolpak.com/shop/page/7/",
    "http://koolpak.com/shop/page/8/"]
    
    

    def parse(self, response):
        print('main_url: '+response.url)

        productLinks = response.xpath(".//h3[@class='product-title']/a/@href").extract()
        

        i = 0 #counter
        
        for linkForEachProducts in productLinks:
            item = ProductsItem()
            productCode_aux, title_aux = response.xpath(".//h3[@class='product-title']/a/text()").extract()[i].split(" ", 1)
            item['Name'] = title_aux
            item['ItemNum'] = productCode_aux

            #contants
            item['ProductID'] = "-1"
            item['CatYear'] = "2018"
            item['ExpirationDate'] = "12/31/2018"
            item['Discontinued'] = "False"
            item['Cat1Name'] = "Bags"
            item['Cat2Name'] = " "
            item['Page1'] = " "
            item['Page2'] = " "
            item['Keywords'] = " "
            item['Themes'] = "Shopping"
            item['Dimension1Units'] = "1"
            item['Dimension1Type'] = "1"
            item['Dimension2Units'] = "1"
            item['Dimension2Type'] = "3"
            item['Dimension3Units'] = "1"
            item['Dimension3Type'] = "4"
            item['Qty1'] = "100"
            item['Qty2'] = "250"
            item['Qty3'] = "500"
            item['Qty4'] = "1000"
            item['Qty5'] = "0"
            item['Qty6'] = "0"
            item['PrCode'] = "RRRR"
            item['PiecesPerUnit1'] = "1"
            item['PiecesPerUnit2'] = "1"
            item['PiecesPerUnit3'] = "1"
            item['PiecesPerUnit4'] = "1"
            item['PiecesPerUnit5'] = "0"
            item['PiecesPerUnit6'] = "0"
            item['QuoteUponRequest'] = "False"
            item['PriceIncludeClr'] = "1 Color"
            item['PriceIncludeSide'] = "1 side"
            item['PriceIncludeLoc'] = "1 location"
            item['SetupChg'] = "45"
            item['SetupChgCode'] = "V"
            item['ScreenChg'] = "0"
            item['ScreenChgCode'] = "0"
            item['PlateChg'] = "0"
            item['PlateChgCode'] = "0"
            item['DieChg'] = "0"
            item['DieChgCode'] = "0"
            item['ToolingChg'] = "0"
            item['ToolingChgCode'] = "0"
            item['RepeatChg'] = "0"
            item['RepeatChgCode'] = "0"
            item['AddClrChg'] = "0"
            item['AddClrChgCode'] = "0"
            item['AddClrRunChg1'] = "0"
            item['AddClrRunChg2'] = "0"
            item['AddClrRunChg3'] = "0"
            item['AddClrRunChg4'] = "0"
            item['AddClrRunChg5'] = "0"
            item['AddClrRunChg6'] = "0"
            item['AddClrRunChgCode'] = "VVVV"
            item['IsRecyclable'] = "False"
            item['IsEnvironmentallyFriendly'] = "False"
            item['IsNewProd'] = "False"
            item['NotSuitable'] = "False"
            item['Exclusive'] = "False"
            item['Hazardous'] = "False"
            item['OfficiallyLicensed'] = "False"
            item['IsFood'] = "False"
            item['IsClothing'] = "False"
            item['ImprintSize1Units'] = "1"
            item['ImprintSize1Type'] = "2"
            item['ImprintSize2Units'] = "1"
            item['ImprintSize2Type'] = "3"
            item['SecondImprintSize1'] = "0"
            item['SecondImprintSize1Units'] = "0"
            item['SecondImprintSize1Type'] = "0"
            item['SecondImprintSize2'] = "0"
            item['SecondImprintSize2Units'] = "0"
            item['SecondImprintSize2Type'] = "0"
            item['SecondImprintLoc'] = ""
            item['NoDecoration'] = "False"
            item['NoDecorationOffered'] = "False"
            item['NewPictureURL'] = " "
            item['NewPictureFile'] = "False"
            item['ErasePicture'] = "False"
            item['NewBlankPictureURL'] = " "
            item['NewBlankPictureFile'] = "False"
            item['EraseBlankPicture'] = "False"
            item['NotPictured'] = "True"
            item['MadeInCountry'] = " "
            item['AssembledInCountry'] = " "
            item['DecoratedInCountry'] = "US"
            item['ComplianceList'] = " "
            item['ComplianceMemo'] = " "
            item['ProdTimeLo'] = "5"
            item['ProdTimeHi'] = "7"
            item['RushProdTimeLo'] = "0"
            item['RushProdTimeHi'] = "0"
            item['Packaging'] = "Bulk"
            item['CartonL'] = "0"
            item['CartonW'] = "0"
            item['CartonH'] = "0"
            item['WeightPerCarton'] = "0"
            item['UnitsPerCarton'] = "0"
            item['ShipPointCountry'] = "US"
            item['ShipPointZip'] = "33020"
            item['Comment'] = "10 Day Production Time For Color Perfect."
            item['Verified'] = "True"
            item['UpdateInventory'] = "False"
            item['InventoryOnHand'] = " "
            item['InventoryOnHandAdd'] = "0"
            item['InventoryMemo'] = " "

            
            
            
            

            
            
            #callback to event page
            request = scrapy.Request(url=linkForEachProducts,
            callback=self.parse_productPage,
            errback=self.errback_httpbin,
            dont_filter=True)
            request.meta['item'] = item


            i = i + 1
            yield request

    def parse_productPage(self,response):
        item = response.meta['item']
        
        
        #Dimensions
        try:
            item['Dimension1'] = re.findall('\d+\.\d+|\d+',response.xpath(".//div[@class='size_product']/p/text()").extract()[0].encode('ascii','ignore'))[0]
        except IndexError:
            item['Dimension1'] = " "
        try:
            item['Dimension2'] = re.findall('\d+\.\d+|\d+',response.xpath(".//div[@class='size_product']/p/text()").extract()[0].encode('ascii','ignore'))[1]
        except IndexError:
            item['Dimension2'] = " "
        
        try:
            item['Dimension3'] = re.findall('\d+\.\d+|\d+',response.xpath(".//div[@class='size_product']/p/text()").extract()[0].encode('ascii','ignore'))[3]
        except IndexError:
            item['Dimension3'] =" "
        
        #prices one color
        item['Prc1'] = response.xpath(".//div[@id='tab-description']/table/tbody/tr[2]/td[3]/text()").extract()[0]
        item['Prc2'] =response.xpath(".//div[@id='tab-description']/table/tbody/tr[2]/td[4]/text()").extract()[0]
        item['Prc3'] = response.xpath(".//div[@id='tab-description']/table/tbody/tr[2]/td[5]/text()").extract()[0]
        item['Prc4'] = response.xpath(".//div[@id='tab-description']/table/tbody/tr[2]/td[6]/text()").extract()[0]
        item['Prc5'] = '0'
        item['Prc6'] = '0'
        #getting color
        item['Colors'] = response.xpath(".//div[@class='Available_Colors']/p/text()").extract()[0]
        #gettind description
        description_aux = ''
        for liFeatured in response.xpath(".//div[@class='Features']/ul//li/text()").extract():
            description_aux = description_aux+', '+ liFeatured
        item['Description'] = description_aux.replace(", ","", 1)
        #getting imprint mode
        item['DecorationMethod'] = response.xpath(".//div[@class='Imprint_Method']/p/text()").extract()[0]
        #Imprint location
        try:
            item['ImprintSize1'] = re.findall('\d+\.\d+|\d+',response.xpath(".//div[@class='Imprint_Area']/p/text()").extract()[0].encode('ascii','ignore'))[0] #add only number
        except IndexError:
            item['ImprintSize1'] = " "
        try:
            item['ImprintSize2'] = re.findall('\d+\.\d+|\d+',response.xpath(".//div[@class='Imprint_Area']/p/text()").extract()[0].encode('ascii','ignore'))[1] #add only number
        except IndexError:
            item['ImprintSize2'] = " "
        try:
            item['ImprintLoc'] = response.xpath(".//div[@class='Imprint_Area']/p/text()").extract()[0].encode('ascii','ignore') #add all detalis number
        except IndexError:
            item['ImprintLoc'] = " "
        
        
        

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

                