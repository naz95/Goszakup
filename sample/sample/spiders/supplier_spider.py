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
    name = "supplier_spider"

    def start_requests(self):
        for i in range(1, 2): # na samom dele 714 stranic
            #url = "https://v3bl.goszakup.gov.kz/ru/register/supplierreg?name_bin_iin_rnn=&country=&region_supplier=19&attribute=3&is_supplier=1&page=%d" % i
            url="https://v3bl.goszakup.gov.kz/ru/register/supplierreg?name_bin_iin_rnn=&country=&region_supplier=&attribute=3&is_supplier=1&page=%d" % i
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
            item['RNN'] = table.select("tr")[5].select("td")[0].text
            item['name_kaz'] = table.select("tr")[6].select("td")[0].text
            item['name_rus'] = table.select("tr")[7].select("td")[0].text
            item['resid'] = table.select("tr")[8].select("td")[0].text
            item['kato'] = table.select("tr")[9].select("td")[0].text
            table1 = soup.select("table.table-striped")[2]
            item['IIN'] = table1.select("tr")[0].select("td")[0].text
            item['RNN1'] = table1.select("tr")[1].select("td")[0].text
            item['FIO'] = table1.select("tr")[2].select("td")[0].text
            table2 = soup.select("table.table-striped")[3]
            item['full_addr_rus'] = table2.select("tr")[1].select("td")[2].text
            item['full_addr_kaz'] = table2.select("tr")[1].select("td")[3].text.encode(
                'utf-8')  # vse ravno russkii ne chitaet
            item['addr_type'] = table2.select("tr")[1].select("td")[4].text.encode('utf-8')
            yield item

