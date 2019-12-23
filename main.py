from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson_h_h import settings
from lesson_h_h.spiders.hh import HhSpider

if __name__=='__main__':
    cr_settings=Settings()
    cr_settings.setmodule(settings)
    process=CrawlerProcess(settings=cr_settings)
    process.crawl(HhSpider)
    process.start()