from scrapy.item import Item, Field

    
class EventsItem(Item):
    #REQUIRED FIELDS
    organization = Field() #This field should contain the name of the organization that is hosting the event! CAN BE HARD-CODED!
    description = Field()
    title = Field()
    ticketUrl = Field() #URL of RSVP or event registration. Use 'eventWebsite' field if unavailable
    eventWebsite = Field()
    In_group_id = Field() #This field should be located in every and each scraper! Just insert it and leave it empty = ""!
    startTime = Field()
    dateFrom = Field() ## DD/MM/YY
    street = Field()
    city = Field()
    state = Field()
    zipCode = Field()
    

    #These are OPTIONAL FIELDS! - If available please insert them
    dateTo = Field()
    endTime = Field()
    eventTimeZone = Field()#Ignore if all events take place in New York 
    noEvents = Field()  #If number of events is listed on page
    location = Field()#Name of location venue or "Online" if a webinar/online event
    room = Field() #If event has a room number/name where is being hosted:
    eventImage = Field() #Include multiple images associated with event (e.g. eventImage1, eventImage2)
    eventAgenda = Field() #Include agenda in description (above) and separately in this field
    contactFirstName = Field()
    contactLastName = Field()
    contactEmail = Field()    #Email can be either a contact email or for general event inquiries
    speakerFirstName = Field()    #If multiple speakers use "speaker1FirstName", "speaker2FirstName" .... and so on
    speakerLastName = Field()     #
    speakerJobTitle = Field()
    speakerAffiliation = Field()
    speakerBio = Field()
    speakerRelatedImage = Field()
    #Most events are free so this field will almost always be blank
    eventPrice = Field()  #(numeric and should contain the dollar sign-eg.: $12.95) 
    #If different prices for members, non-members, students, etc..
    #If you use this type of Prices .... than you do not need to insert the "eventPrice" from above 
    eventPriceMembers = Field()
    eventPriceStudents = Field()
    eventPriceNonmembers = Field()
    eventTags = Field()
    hashtags = Field() #(text format - comma separated event tags)
    #If event has social pages please gather the url and use:
    eventFlink = Field()   #(Facebook link)
    eventTlink = Field()   #(Twitter link)
    eventIlink = Field()  #(Instagram link)



    last_updated = Field(serializer=str)
    pass