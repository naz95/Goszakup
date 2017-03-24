import scrapy
from scrapy.spider import CrawlSpider
from scrapy import Item, Field


class Company(scrapy.Item):
    BIN = Field()
    RNN = Field()
    name_kaz = Field()
    name_rus= Field()
    resid = Field()
    kato = Field()
    IIN = Field()
    RNN1 = Field()
    FIO = Field()
    full_addr_rus = Field()
    full_addr_kaz = Field()
    addr_type = Field()


class MySpider(CrawlSpider):
    name = "goszakup1"
    start_urls = ["https://v3bl.goszakup.gov.kz/ru/register/supplierreg/show/189817"]

    def parse(self, response):
        # response.xpath('//div[@class="text1"][1]/h3/a/text()')
        titles = response.xpath('//div[@class="panel panel-default"]')
        items = []
        # for title in titles:
        item = Company()
        item['BIN'] = titles[0].xpath('div[@class="panel-body"]/table/tr[5]/td/text()').extract()
        item['RNN'] = titles[0].xpath('div[@class="panel-body"]/table/tr[6]/td/text()').extract()
        item['name_kaz'] = titles[0].xpath('div[@class="panel-body"]/table/tr[7]/td/text()').extract_first().encode(
            'utf-8')
        item['name_rus'] = titles[0].xpath('div[@class="panel-body"]/table/tr[8]/td/text()').extract_first().encode(
            'utf-8')
        item['resid'] = titles[0].xpath('div[@class="panel-body"]/table/tr[9]/td/text()').extract_first().encode(
            'utf-8')
        item['kato'] = titles[0].xpath('div[@class="panel-body"]/table/tr[10]/td/text()').extract()
        item['IIN'] = titles[2].xpath('div[@class="panel-body"]/table/tr[1]/td/text()').extract()
        item['RNN1'] = titles[2].xpath('div[@class="panel-body"]/table/tr[2]/td/text()').extract()
        item['FIO'] = titles[2].xpath('div[@class="panel-body"]/table/tr[3]/td/text()').extract_first().encode('utf-8')
        item['full_addr_rus'] = titles[3].xpath(
            'div[@class="panel-body"]/table/tr[2]/td[3]/text()').extract_first().encode('utf-8')
        item['full_addr_kaz'] = titles[3].xpath(
            'div[@class="panel-body"]/table/tr[2]/td[4]/text()').extract_first().encode('utf-8')
        item['addr_type'] = titles[3].xpath(
            'div[@class="panel-body"]/table/tr[2]/td[5]/text()').extract_first().encode('utf-8')

        yield item