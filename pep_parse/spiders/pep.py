import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import ALLOWED_DOMAINS


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ALLOWED_DOMAINS
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        numerical_index_peps_table = response.css(
            'section[id="numerical-index"]').css('a[href^="pep"]')
        for pep_link in numerical_index_peps_table[0:]:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = ' '.join((response.css(
            'h1[class="page-title"]::text').get()).split()[:2])
        name = ' '.join((response.css(
            'h1[class="page-title"]::text').get()).split()[3:])
        data = {
            'status': response.css('abbr::text').get(),
            'name': name,
            'number': number,
        }
        yield PepParseItem(data)
