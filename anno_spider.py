import scrapy
from scrapy.spider import CrawlSpider
from scrapy import Item, Field

class Annos1(scrapy.Item):

	num = Field()
	organizer = Field()
	name = Field()
	zakup = Field()
	ztype = Field()
	start_date = Field()
	end_date = Field()
	anno_amt = Field()
	summa = Field()
	status = Field()

class MySpider(CrawlSpider):
	name = "anno"
	start_urls = ["https://v3bl.goszakup.gov.kz/ru/searchanno"]

	def parse(self, response):
		
		annos = response.xpath('//table[@class="table table-bordered"]/tr')[1:]

		for anno in annos:
			item = Annos1()
			item['num']=anno.xpath('td[1]/text()').extract_first().strip()
			item['organizer']=anno.xpath('td[2]/text()').extract_first().strip()
			item['name']=anno.xpath('td[3]/a/div[2]/text()').extract_first().strip()
			item['zakup']=anno.xpath('td[4]/text()').extract_first().strip()
			item['ztype']=anno.xpath('td[5]/text()').extract_first().strip()
			item['start_date']=anno.xpath('td[6]/text()').extract_first().strip()
			item['end_date']=anno.xpath('td[7]/text()').extract_first().strip()
			item['anno_amt']=int(anno.xpath('td[8]/text()').extract_first().strip())
			item['summa']=float(anno.xpath('td[9]/text()').extract_first().strip().replace(" ",""))
			item['status']=anno.xpath('td[10]/text()').extract_first().strip()
		
			yield item

		#next_page = response.xpath('//ul[@class="pagination"]/li/a/@href').extract()[-1]
		#if next_page:
		#	yield scrapy.Request(response.urljoin(next_page),callback=self.parse)