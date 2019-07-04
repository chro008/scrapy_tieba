# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from Tieba.items import TiebaItem


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    categorys = ["安国", "安新", "博野", "定兴", "阜平", "高碑店", "高阳",
                 "涞水", "涞源", "蠡县", "满城", "清苑", "曲阳", "容城", "顺平", "唐县", "望都", "雄县",
                 "徐水", "保定", "易县", "涿州"]

    base_url = 'http://tieba.baidu.com/f?ie=utf-8&kw='
    start_urls = []
    for index in range(len(categorys)):
        start_urls.append(base_url + categorys[index])

    def parse(self, response):

        for each in response.xpath("//*[@id='thread_list']//li"):
            item = TiebaItem()
            title = each.xpath("div/div[2]/div[1]/div[1]/a").css("::text").extract_first()
            url = each.xpath("div/div[2]/div[1]/div[1]/a").css("::attr(href)").extract_first()
            item['url'] = url
            item['title'] = title
            item['category'] = urllib.parse.unquote(response.url.split("&kw=")[1].split("&")[0])
            yield item

        urls = response.url.split("&pn=")
        base_url = urls[0]
        page_limit = 0
        # 爬取的分页 页面数
        pages = 4
        if len(urls) > 1:
            page_limit = int(urls[1])

        if page_limit < (pages - 1) * 50:
            page_limit = str(page_limit + 50)
            next_page = base_url + "&pn=" + page_limit
            print("ready to scrapy next page:" + page_limit)
            yield scrapy.Request(next_page, callback=self.parse)
