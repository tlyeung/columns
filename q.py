import scrapy
from scrapy.http import HtmlResponse
import requests
from shutil import copyfile
from datetime import datetime

class AppleSpider(scrapy.Spider):
    name = "apple"

    def start_requests(self):
        urls = [
            'https://hk.lifestyle.appledaily.com/lifestyle/columnist/index/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'col.txt'
        authors = response.css('div.bluebox div.col02 div.author a::text').getall()
        titles = response.css('div.bluebox div.col02 div.title a::text').getall()
        urls = response.css('div.bluebox div.col02 div.title a::attr(href)').getall()
        with open(filename, 'wb') as f:
            for a in range(len(authors)):
                f.write(authors[a].encode('utf-8'))
                f.write('  '.encode())
                f.write(titles[a].encode())
                f.write('\n'.encode())
                f.write('\n'.encode())
                c_response = HtmlResponse(
                        url = urls[a],
                        body = requests.get(url=urls[a]).content,
                        )
                p = (c_response.css('div.ArticleContent_Inner p').getall()[1][3:-300]).strip()
                f.write(p.replace("<br>","\n").encode())
                f.write('\n'.encode())
                f.write('\n'.encode())
                f.write('\n'.encode())
                f.write('\n'.encode())
        self.log('Saved file %s' % filename)
        now = datetime.now()
        copyfile(filename, "col_{}.txt".format(now.strftime("%Y%m%d")))
