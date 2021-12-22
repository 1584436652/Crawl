import scrapy
import re
from ..items import ArticleItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    page = 1
    allowed_domains = ['www.meiwenjx.com']
    start_urls = []
    article_url = 'https://www.meiwenjx.com/{}'
    home_url = 'https://www.meiwenjx.com/renshengganwu/renshengzheli/list_{}.html'
    read_count_url = 'https://www.meiwenjx.com/plus/count.php?view=yes&aid={}&mid=1'

    def start_requests(self):
        yield scrapy.Request(url=self.home_url.format(self.page), callback=self.parse)

    def parse(self, response):
        self.page += 1
        resp = response.xpath('//div[@class="listbox"]//div[@class="listitem"]/ul/li')
        for r in resp:
            item = ArticleItem()
            print('1111')
            link = r.xpath('./a/@href').extract_first()
            a_id = re.findall(r'e/(.*?).html', link)[0]
            yield scrapy.Request(response.urljoin(self.read_count_url.format(a_id)), self.article_detail_parse)
            item['title'] = link
            yield item

        # if self.page < 5:
        #     yield scrapy.Request(self.home_url.format(self.page), callback=self.parse)

    def article_detail_parse(self, response):
        item = ArticleItem()
        count = re.findall(r"'(.*?)'", response.text)[0]
        print(response.url, count)
        item['messages'] = count
        yield item















