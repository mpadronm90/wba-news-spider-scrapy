import scrapy

class NewsSpiderItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()