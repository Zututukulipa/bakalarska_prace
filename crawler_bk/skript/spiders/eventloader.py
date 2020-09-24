from price_parser import Price
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
from skript.items import Event


def get_price_value(input_value):
    price = Price.fromstring(input_value)
    if price.amount is None:
        return 0
    return price.amount


def get_price_currency(input_value):
    if isinstance(input_value, list):
        for pricetag in input_value:
            price = Price.fromstring(pricetag)
            if price.currency:
                return price

    price = Price.fromstring(input_value)
    if price.currency is None:
        return 'NOT_FOUND'
    return price.currency


class EventLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = Event
    title_in = MapCompose(str.strip, remove_tags)
    description_in = MapCompose(str.strip, remove_tags)
    address_in = MapCompose(str.strip, remove_tags)
    description_out = Join()
    pricing_min_in = MapCompose(get_price_value)
    pricing_max_in = MapCompose(get_price_value)
    pricing_currency_in = MapCompose(get_price_currency)
    address_out = Join()