import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f'https://www.worldometers.info{link}'
            # absolute_url = response.urljoin(link)

            # yield scrapy.Request(url=absolute_url)

            # yield {
            #     'country_name': name,
            #     'country_link': link,
            # }
            # after scrapy sends request to each country link response will be sent to parse_country method
            yield response.follow(url=link, callback=self.parse_country)

    def parse_country(self, response):
        # logging.info(response.url) logging the info for each response we get
        rows = response.xpath(
            '//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'year': year,
                'population': population
            }
