# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from lesson_h_h.items import LessonHHItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['vladivostok.hh.ru']
    list_vacantion = ['Бухгалтер', 'Программист', 'Менеджер+по+продажам']
    ## 22 код региона 1- Москва 2 Санкт-Петербург
    region = 22
    start_urls = [
        f'https://vladivostok.hh.ru/search/vacancy?area=22&items_on_page=20&st=searchVacancy&text={i}&customDomain=1'
        for i in list_vacantion]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[contains(@class,"bloko-button HH-Pager-Controls-Next HH-Pager-Control")]/@href').extract_first()
        job_openings = response.xpath('//a[contains(@class,"bloko-link HH-LinkModifier")]/@href').extract()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        print(len(job_openings))
        for vacancy in job_openings:
            print(vacancy)
            yield response.follow(vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item = ItemLoader(LessonHHItem(), response)
        item.add_xpath('title', '//h1[contains(@class,"header")]/span/text()')
        item.add_value('url', response.url)
        item.add_xpath('description',
                       '//div[contains(@class,"vacancy-section")]/div[contains(@class,"g-user-content")]')
        item.add_xpath('salary', '//p[@class="vacancy-salary"]')
        item.add_xpath('employer', '//a[@class="vacancy-company-name"]/span')
        item.add_xpath('employer_url', '//a[@class="vacancy-company-name"]/@href')
        yield item.load_item()
