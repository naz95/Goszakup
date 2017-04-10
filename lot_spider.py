import scrapy
from scrapy.spider import CrawlSpider
from scrapy import Item, Field

class Lotts(scrapy.Item):

	lotnum = Field()
	requestor = Field()
	name = Field()
	desc = Field()
	zakup = Field()
	plan_date = Field()
	amount = Field()
	price = Field()
	summa = Field()
	status = Field()
	req_amount = Field()

class MySpider(CrawlSpider):
	name = "lots"
	start_urls = ["https://v3bl.goszakup.gov.kz/ru/subpriceoffer"]

	def parse(self, response):
		
		lots = response.xpath('//table[@class="table table-bordered"]/tr')[1:]

		for lot in lots:
			item = Lotts()
			item['lotnum']=lot.xpath('td[2]/a/text()').extract_first()
			item['requestor']=lot.xpath('td[3]/text()').extract_first().strip()
			item['name']=lot.xpath('td[4]/div/a/text()').extract_first().strip()
			item['desc']=lot.xpath('td[5]/text()').extract_first().strip()
			item['zakup']=lot.xpath('td[6]/text()').extract_first().strip()
			item['plan_date']=lot.xpath('td[7]/text()').extract_first()
			item['amount']=int(lot.xpath('td[8]/text()').extract_first())
			item['price']=float(lot.xpath('td[9]/text()').extract_first())
			item['summa']=float(lot.xpath('td[10]/text()').extract_first())
			item['status']=lot.xpath('td[11]/text()').extract_first().strip()
			item['req_amount']=int(lot.xpath('td[12]/text()').extract_first())
		
			yield item

		#next_page = response.xpath('//ul[@class="pagination"]/li/a/@href').extract()[-1]
		#if next_page:
		#	yield scrapy.Request(response.urljoin(next_page),callback=self.parse)