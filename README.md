# bakalarska_prace
Created scripts were created to scrap data about public events on four selected ticket vendors. Scraped data is stored into CassandraDB, running in docker instance and visualized in added Zeppelin container. Both services can be called with `docker-compose up` in `docker` directory.
## calling scripts
To call script use `scrapy crawl <name_of_crawler>` in `skript` directory.
Names for created scripts are:
* kudyznudy
* goout
* ticketportal
* ticketstream
