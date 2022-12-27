import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a.pep.reference.internal::attr(href)')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': int(
                response.css('h1.page-title::text').get().strip().split()[1]
            ),
            'name': ' '.join(
                response.css('h1.page-title::text').get().strip().split()[3:]),
            'status': response.css('abbr::text').get().strip(),
        }
        return PepParseItem(data)
