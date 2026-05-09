import scrapy

class JobItem(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    sector = scrapy.Field()
    function = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    contract = scrapy.Field()
    url = scrapy.Field()