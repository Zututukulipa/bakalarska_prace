from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import SitemapSpider, Rule
from skript.items import Event
from skript.spiders.eventloader import EventLoader


class GooutSpider(SitemapSpider):
    name = "goout"
    sitemap_urls = ['https://goout.net/i/sitemaps/event-CS-0.xml']
    rules = (
        Rule(LinkExtractor(allow=('/kultura-online/', '/divadlo/', '/vystavy/', '/koncerty/', '/jine-akce/',
                                  '/parties/', '/festivaly/', '/gastro/', '/pro-deti/',
                                  '/vstupenky/', '/akce/')),)
    )

    def parse(self, response):
        loader = EventLoader(item=Event(), response=response)

        loader.add_value('url', response.url)

        loader.add_xpath(
            'title', "//div[@class='eventHeadline-text ']/h1/text()")
        loader.add_xpath(
            'time', "//meta[@itemprop='startDate']/@content")
        loader.add_xpath(
            'description', "//div[@class='textAboutItem']/p/text()")
        price = response.xpath(
            "//span[contains(@id, 'pricing')]/text()").extract()

        if "–" in price:
            prices = price.split(chr(8211))
            loader.add_value('pricing_min', prices[0])
            loader.add_value('pricing_currency', price[0])
            loader.add_value('pricing_max', prices[1])
        else:
            loader.add_value('pricing_min', price)
            loader.add_value('pricing_currency', price)
            loader.add_value('pricing_max', price)

        loader.add_xpath(
            'address', "//span[contains(@itemprop, 'ddress')]/text()")
        loader.add_value('label', urlparse(response.url).netloc)

        return loader.load_item()
