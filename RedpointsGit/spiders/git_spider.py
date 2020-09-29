import scrapy
import urllib


class GitSpider(scrapy.Spider):

    # Name of the spider
    name = "git"
    # Base url to start crawling
    BASE_URL = 'https://github.com'

    def __init__(self, query, proxy, search_type, *args, **kwargs):
        super(GitSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.search_type = search_type
        self.proxy = proxy

    def start_requests(self):
        """ Initial request to github to get the list of urls """
        params = {
            'q': self.query,
            'type': self.search_type
        }
        url = f'{self.BASE_URL}/search?{urllib.parse.urlencode(params)}'
        request = scrapy.Request(url, callback=self.parse)
        request.meta['params'] = params
        request.meta['proxy'] = self.proxy

        return [request]

    def parse_repositories(self, response):
        """ Parse request to get urls and extras for repository crawling, called from method parse """
        language_stats = response.xpath('//span[contains(@class,"Progress-item")]/@aria-label').getall()
        yield {
            'url': response.request.url,
            'extra': {
                'owner': str.split(response.request.url, '/')[3],
                'language_stats': {
                    str.split(language_stat)[0]: float(str.split(language_stat)[1]) for language_stat in language_stats
                }
            }
        }

    def parse(self, response, **kwargs):
        """ Parse first request to get the urls and make request for repository crawling """
        urls = response.xpath(
            '//div[contains(@class, "results")]//a[contains(@data-hydro-click, "search_result.click")]//@href')\
            .getall()
        if str.lower(self.search_type) != 'repositories':
            for url in urls:
                absolute_url = self.BASE_URL + url
                yield {
                    'url': absolute_url
                }
        else:
            for url in urls:
                absolute_url = self.BASE_URL + url
                yield scrapy.Request(
                    absolute_url,
                    callback=self.parse_repositories,
                    meta={"proxy": self.proxy}
                )
