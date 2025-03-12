import scrapy


class HotelItem(scrapy.Item):
    hotel_name = scrapy.Field()
    price = scrapy.Field()
