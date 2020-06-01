# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//td[@class="titleColumn"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield{
            'title': response.xpath('//div[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath('//span[@id="titleYear"]/a/text()').get(),
            'rating': response.xpath('//span[@itemprop = "ratingValue"]/text()').get(),
            'duration': response.xpath('(//time)[1]/text()').get().replace("\n", "").replace(" ", "").replace("h", "h "),
            'genre': response.xpath('//div[@class="subtext"]/a[1]/text()').get(),
            'movie url': response.url,
            'trailer url': response.urljoin(response.xpath('//a[@class="slate_button prevent-ad-overlay video-modal"]/@href').get())
        }
