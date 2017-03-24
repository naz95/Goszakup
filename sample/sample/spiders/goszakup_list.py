import scrapy
from scrapy.spider import CrawlSpider
from scrapy import Item, Field
from bs4 import BeautifulSoup

class Supplier(scrapy.Item):
    id = Field()
    name=Field()

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
    name = "goszakup"

    def start_requests(self):
        for i in range(1, 2):
            url = "https://v3bl.goszakup.gov.kz/ru/register/supplierreg?name_bin_iin_rnn=&country=&region_supplier=19&attribute=3&is_supplier=1&page=%d" % i
            request = scrapy.Request(url, callback=self.parse_page)
            yield request


    def parse_page(self, response):
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        trs = soup.select("table.table-bordered tr")[1:]
        for tr in trs:
            item = Supplier()
            id = int(tr.select('td')[0].text)
            item['id'] = id
            item['name'] = tr.select("td a")[0].text
            url = "https://v3bl.goszakup.gov.kz/ru/register/supplierreg/show/%d" % id
            request = scrapy.Request(url, callback=self.parse_item)
            request.meta['item']  = item
            yield request

    def parse_item(self, response):
            supplier = response.meta['item']
            html  = response.text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.select("table.table-striped")[0]
            # for title in titles:
            item = Company()
            item['BIN'] = table.select("tr")[4].select("td")[0].text
            #item['RNN'] = table.select("tr")[5].select("td")[0].text
           # item['name_kaz'] = table.select ("tr")[6].select("td")[0].text
           # item['name_rus'] = table.select("tr")[7].select("td")[0].text
           # item['resid'] = table.select("tr")[8].select("td")[0].text
            #item['kato'] = table.select("tr")[9].select("td")[0].text
            table1 = soup.select("div.panel-body")[0]
            item['IIN'] = table1.select("tr")[0].select("td")[0].text
           # item['RNN1'] = titles[2].xpath('div[@class="panel-body"]/table/tr[2]/td/text()').extract()
           # item['FIO'] = titles[2].xpath('div[@class="panel-body"]/table/tr[3]/td/text()').extract_first().encode('utf-8')
           # item['full_addr_rus'] = titles[3].xpath(
           # 'div[@class="panel-body"]/table/tr[2]/td[3]/text()').extract_first().encode('utf-8')
           # item['full_addr_kaz'] = titles[3].xpath(
           # 'div[@class="panel-body"]/table/tr[2]/td[4]/text()').extract_first().encode('utf-8')
           # item['addr_type'] = titles[3].xpath(
           # 'div[@class="panel-body"]/table/tr[2]/td[5]/text()').extract_first().encode('utf-8')
            yield item
