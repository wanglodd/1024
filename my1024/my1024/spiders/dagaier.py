# -*- coding: utf-8 -*-
import scrapy

from my1024.items import dagaierItem


class DagaierSpider(scrapy.Spider):
    name = "dagaier"
    allowed_domains = ["t66y.com"]
    start_urls = [
        'http://t66y.com/thread0806.php?fid=16&search=&page=1'
    ]
    unicode_next = u'\u4e0b\u4e00\u9801'

    def parse(self, response):
        thread_hrefs = response.selector.xpath('//h3/a/@href')
		
        for thread_href in thread_hrefs:
            thread_url = response.urljoin(thread_href.extract())
            yield scrapy.Request(thread_url, callback=self.parse_thread)

        next_href = response.selector.xpath(
            "//a[text()='%s']/@href" % self.unicode_next)[0]
        next_url = response.urljoin(next_href.extract())

        yield scrapy.Request(next_url, callback=self.parse)

    def parse_thread(self, response):
        item = dagaierItem()
        item['tit'] = response.selector.xpath(
            'string(//title)')[0].extract()
        item['img'] = response.selector.xpath(
            '//input/@src').extract()
        yield item
