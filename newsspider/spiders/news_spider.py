import scrapy
from newsspider.items import NewsSpiderItem

class NewsSpider(scrapy.Spider):
    name = 'newsspider'

    def __init__(self, url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        item = NewsSpiderItem()

        # Extract the title
        item['title'] = response.css('title::text').get() or response.xpath('//h1/text()').get()

        # Extract the author
        item['author'] = response.css('meta[name="author"]::attr(content)').get() or \
                         response.css('.author-name::text').get() or \
                         response.xpath('//span[@class="author"]/text()').get()

        # Extract the publish date
        item['publish_date'] = response.css('meta[name="publish_date"]::attr(content)').get() or \
                               response.css('.publish-date::text').get() or \
                               response.xpath('//time[@class="published"]/text()').get()

        # Try different selectors for the content
        content_selectors = [
            '//article//p//text()',
            '//div[contains(@class,"article-content")]//p//text()',
            '//div[contains(@class,"post-content")]//p//text()',
            '//div[contains(@class,"content")]//p//text()',
            '//div[contains(@class,"entry-content")]//p//text()',
        ]

        content = None
        for selector in content_selectors:
            content = response.xpath(selector).getall()
            if content:
                break

        # If no specific selectors worked, fallback to the body tag
        if not content:
            content = response.xpath('//body//text()').getall()

        # Clean and join the content
        cleaned_content = ' '.join([text.strip() for text in content if text.strip()])

        # Assign the cleaned content to the item
        item['content'] = cleaned_content
        item['url'] = response.url

        yield item
