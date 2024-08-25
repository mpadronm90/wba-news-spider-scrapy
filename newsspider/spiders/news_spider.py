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

        # Improved content selection logic targeting deeper nested structures
        content_selectors = [
            '//div[contains(@class,"article-content")]//p//text() | //div[contains(@class,"article-content")]//div//text()',
            '//div[contains(@class,"post-content")]//p//text() | //div[contains(@class,"post-content")]//div//text()',
            '//div[contains(@class,"content")]//p//text() | //div[contains(@class,"content")]//div//text()',
            '//div[contains(@class,"entry-content")]//p//text() | //div[contains(@class,"entry-content")]//div//text()',
            '//article//p//text() | //article//div//text()',
            '//div[contains(@class,"MainStory_storycontent")]//p//text() | //div[contains(@class,"MainStory_storycontent")]//div//text()',
        ]

        content = []
        for selector in content_selectors:
            section_content = response.xpath(selector).getall()
            if section_content:
                content.extend(section_content)

        # If no specific selectors worked, fallback to broader selection, but still target relevant tags
        if not content:
            content = response.xpath('//body//p//text() | //body//div[contains(@class,"content")]//text()').getall()

        # Function to filter out irrelevant content like disclaimers, related news, or promotional sections
        def is_relevant_text(text):
            # Remove text that contains typical "noise" like "Also Read", "LIVE updates", "Disclaimer", etc.
            noise_keywords = [
                "also read", "live news updates", "disclaimer", "click here", "connect with us", "powered by", "recommend",
                "streaming", "full list of teams", "owner details", "related news", "share this", "follow us"
            ]
            # Exclude text based on these keywords
            if any(keyword in text.lower() for keyword in noise_keywords):
                return False
            # Exclude very short lines or lines that are likely headers or navigation links
            if len(text.split()) < 5:  # Fewer than 5 words is often non-content
                return False
            return True

        cleaned_content = [text.strip() for text in content if text.strip() and is_relevant_text(text)]

        # Remove duplicate sections or lines
        final_content = []
        seen_lines = set()
        for line in cleaned_content:
            if line not in seen_lines and len(line) > 20:  # Avoid very short lines
                final_content.append(line)
                seen_lines.add(line)

        # Assign the cleaned content to the item
        item['content'] = ' '.join(final_content)
        item['url'] = response.url

        yield item

