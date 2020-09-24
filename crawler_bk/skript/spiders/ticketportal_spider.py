from urllib.parse import urlparse

from scrapy.spiders import SitemapSpider

from skript.items import Event
from skript.spiders.eventloader import EventLoader


class TicketPortalSpider(SitemapSpider):
    name = "ticketportal"
    sitemap_urls = ['https://www.ticketportal.cz/robots.txt']
    sitemap_rules = [('/event/', 'parse'), ('/nevent/', 'parse')]

    def parse(self, response):
        if "PARKOVACI" in response.url:
            return None
        loader = EventLoader(item=Event(), response=response)

        loader.add_value('url', response.url)

        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('time', "//section//tr/td[2]/text()")
        loader.add_xpath('description', "//*[@class='popis']/p/text()")

        loader.add_xpath('address', "//td/a/text()")
        loader.add_value('label', urlparse(response.url).netloc)

        return loader.load_item()
