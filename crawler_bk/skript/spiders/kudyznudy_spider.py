import scrapy
from scrapy.spiders import Spider
from datetime import date, timedelta
from skript.items import Event
from skript.spiders.eventloader import EventLoader
from urllib.parse import urlparse


def generate_scrape_dates(amount):
    mounting_day = date.today()
    # EXAMPLE: "https://www.kudyznudy.cz/kalendar-akci?datum=2020-02-25"
    search_string = "https://www.kudyznudy.cz/kalendar-akci?datum={}"
    urls_to_parse = []
    for x in range(1, amount):
        dt = mounting_day + timedelta(x)
        urls_to_parse.append(search_string.format(dt.strftime("%Y-%m-%d")))
    return urls_to_parse


def extract_date(date_array):
    date_length = len(date_array)
    if date_length > 8:
        date = "{}{}{}{}{}{}{}".format(date_array[3], date_array[4], date_array[5], date_array[6],
                                       date_array[7], date_array[8], date_array[9])
    elif date_length == 4:
        date = "{}{}".format(date_array[3], date_array[4])
    else:
        date = "{}{}{}".format(date_array[3], date_array[4], date_array[5])
    return date


class QuotesSpider(Spider):
    name = "kudyznudy"

    def __init__(self, days=31, *args, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = generate_scrape_dates(int(days))

    def parse(self, response):
        for event in response.xpath("//div[@class='item one-fourth']/a/@href").extract():
            yield scrapy.Request("https://" + urlparse(response.url).netloc + event, callback=self.parse_event)

    def parse_event(self, response):
        loader = EventLoader(item=Event(), response=response)

        loader.add_value('url', response.url)

        loader.add_xpath('title', "//h1[@class='title j-documentTitle']/text()")

        extracted_date = response.xpath("//span[@class='date-info']//text()").extract()

        loader.add_value('time', extract_date(extracted_date))

        loader.add_xpath('description', "//div[contains(@class, 'annotation')]/text()")
        loader.add_xpath('pricing_min', "//span[@class='fright']/text()[1]")
        loader.add_xpath('pricing_currency', "//span[@class='fright']/text()[1]")
        loader.add_xpath('pricing_max', "//span[@class='fright']/text()[1]")
        loader.add_xpath('address', "//address/text()")
        loader.add_value('label', self.name)

        yield loader.load_item()
