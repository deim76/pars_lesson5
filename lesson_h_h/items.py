# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def cleaner_text_symbol(result: str):
    list_symbol = ['strong>','div>','br>','ul>','li>','<p', '/p>','span','<', '/', '!', '--',  '>', 'itemprop="name"',
                   'class="vacancy-salary"']
    for symbol in list_symbol:
        result = result.replace(symbol, '')

    return result


def cleaner_text_description(item):
    result = item.split('<strong><span>')[1:]
    key = 'description'
    value = ''
    for item_text in result:
        value += cleaner_text_symbol(item_text)

    return {key: value}


def cleaner_text_employer(item):
    return cleaner_text_symbol(item[0])


def text_salary(item):
    result = 'None'
    if 'от' in item[0]:
        result = cleaner_text_symbol(item[0])

    return result


class LessonHHItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(cleaner_text_description), output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=text_salary, output_processor=TakeFirst())
    employer = scrapy.Field(input_processor=cleaner_text_employer, output_processor=TakeFirst())
    employer_url = scrapy.Field(output_processor=TakeFirst())

