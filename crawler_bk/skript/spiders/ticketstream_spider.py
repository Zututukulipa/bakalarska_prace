from scrapy.spiders import SitemapSpider
from skript.items import Event
from skript.spiders.eventloader import EventLoader


class QuotesSpider(SitemapSpider):
    name = "ticketstream"
    sitemap_urls = ['https://www.ticketstream.cz/robots.txt']
    sitemap_rules = [('/akce/', 'parse')]

    def parse(self, response):
        loader = EventLoader(item=Event(), response=response)

        loader.add_value('url', response.url)

        loader.add_xpath('title', "//*[@id='event-name']/text()")
        loader.add_xpath('time', "//meta[@itemprop='startDate']/@content")
        loader.add_xpath('description', "//div[@itemprop='description']/p/text()")
        loader.add_xpath('pricing_min', "//div[@data-price-from]/@data-price-from")
        loader.add_xpath('pricing_currency', "//div[@data-price-from]/@data-price-currency")
        loader.add_xpath('pricing_max', "//div[@data-price-from]/@data-price-to")

        city = response.xpath("(//div[@class='meta-container']/h2/text())[1]").extract()
        street = response.xpath("//meta[@itemprop='streetAddress']/@content").extract()
        zipcode = response.xpath("//meta[@itemprop='postalCode']/@content").extract()

        addr = "{} {} {}".format(street[0], city[0], zipcode[0])

        loader.add_value('address', addr)
        loader.add_value('label', self.name)

        return loader.load_item()


