# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from javspider.items import JavspiderItem


class JavSpider(CrawlSpider):
    name = 'jav'
    allowed_domains = ['dmmsee.net']
    offset = 1
    url = 'https://www.dmmsee.net/genre/e/'
    start_urls = [url+str(offset)]

    rules = (
        Rule(LinkExtractor(allow=r'https://www.dmmsee.net/\w+-\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = JavspiderItem()
        item['car_id'] = response.xpath('//div[@class="col-md-3 info"]//span/text()').extract()[1]
        item['download_link'] = response.xpath("//div[@class='movie']//a/@href").extract()[0]
        img_list = response.xpath("//div[@id='sample-waterfall']//a/@href").extract()
        if img_list == []:
            item["img_link"] = '无插图'
        else:
            item["img_link"] = img_list
        yield item

        if self.offset <= 2:
            self.offset += 1
            yield scrapy.Request(self.url+str(self.offset))
