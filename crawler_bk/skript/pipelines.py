# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from cassandra.cluster import Cluster


def set_defaults(item):
    item.setdefault('time', 'NOT_FOUND')
    item.setdefault('title', 'NOT_FOUND')
    item.setdefault('url', 'NOT_FOUND')
    item.setdefault('description', 'NOT_FOUND')
    item.setdefault('pricing_min', 0)
    item.setdefault('pricing_max', 0)
    item.setdefault('label', 'UNKNOWN')
    item.setdefault('address', 'NOT_FOUND')
    item.setdefault('pricing_currency', 'Kč')
    item.setdefault('timestamp', datetime.today())


class CassandraPipeline(object):

    def __init__(self, cassandra_keyspace, cassandra_address, cassandra_port):
        self.cassandra_keyspace = cassandra_keyspace
        cluster = Cluster([cassandra_address], port=cassandra_port)
        self.session = cluster.connect(self.cassandra_keyspace)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cassandra_keyspace=crawler.settings.get('CASSANDRA_KEYSPACE'),
            cassandra_address=crawler.settings.get('CASSANDRA_ADDRESS'),
            cassandra_port=crawler.settings.get('CASSANDRA_PORT')
        )

    def open_spider(self, spider):
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS scraped WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};")
        self.session.execute("CREATE TABLE IF NOT EXISTS"
                             " {}.urls "
                             "( url text, stamp timestamp, label text, PRIMARY KEY(url) )"
                             .format(self.cassandra_keyspace))
        self.session.execute("CREATE TABLE IF NOT EXISTS"
                             " {}.events "
                             "( source_url text, title text,"
                             " address text, date text, description text,"
                             " pricing_min decimal, pricing_max decimal, pricing_currency text,"
                             " label text, stamp timestamp,"
                             " PRIMARY KEY(source_url) )"
                             .format(self.cassandra_keyspace))

    def close_spider(self, spider):
        self.session.shutdown()

    def process_item(self, item, spider):
        set_defaults(item)
        request = self.session.prepare("INSERT INTO {}.events (source_url, title, address, date, description," \
                                       " pricing_min, pricing_max, pricing_currency, label, stamp)" \
                                       " VALUES ('{}', ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(self.cassandra_keyspace,
                                                                                          item['url']))

        self.session.execute(request, [item['title'], item['address'],
                                       item['time'], item['description'],
                                       item['pricing_min'], item['pricing_max'],
                                       item['pricing_currency'], item['label'],
                                       item['timestamp']])

        self.session.execute(request)
        return item
