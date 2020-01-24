import scrapy
import os
import os.path
from scrapy.crawler import CrawlerProcess

class VisitingChefSpider(scrapy.Spider):
	name = 'chefs'
	start_urls = [
        'https://www.rit.edu/fa/diningservices/',
    ]
	
	def parse(self, response):
		for chef in response.css('div.col-xs-12.col-md-6.visitingchef-content'):
			info_element = {
				'name': chef.css('div.visitingchef-event::text').get().strip(),
				'location': chef.css('div.visitingchef-location::text').getall()[1].strip()
            }
			yield info_element


if os.path.exists('data.json'):
	os.remove('data.json')

process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	'FEED_FORMAT': 'json',
	'FEED_URI': 'data.json'
})

process.crawl(VisitingChefSpider)
process.start()

os.rename('data.json', '/remote/testapi/Main/data.json')
