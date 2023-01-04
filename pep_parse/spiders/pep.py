import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        table = response.css('#numerical-index').css('tr')
        for tr in table:
            try:
                pep_link = tr.css('a').attrib['href']
                yield response.follow(pep_link, callback=self.parse_pep)
            except KeyError:
                continue

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
