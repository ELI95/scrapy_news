import datetime

from scrapy import Spider

from scrapy_news.items import ScrapyNewsItem


def get_publish_datetime(publish_time):
    publish_date = datetime.date.today().strftime('%Y-%m-%d')
    publish_datetime = datetime.datetime.strptime(publish_date + ' ' + publish_time, '%Y-%m-%d %H:%M')
    if publish_datetime > datetime.datetime.now():
        return
    return publish_datetime


def get_items(news_items, resource, category, crawl_number):
    items = list()
    for news_item in news_items[:crawl_number]:
        item = ScrapyNewsItem()
        item['content'] = news_item.xpath('div[@class="news_content"]/text()').extract_first()
        publish_time = news_item.xpath('div[@class="news_datetime"]/text()').extract_first()
        publish_datetime = get_publish_datetime(publish_time)
        if not publish_time:
            continue
        item['publish_datetime'] = publish_datetime
        item['resource'] = resource
        item['category'] = category
        item['timestamp'] = datetime.datetime.now()
        items.append(item)
    return items


class NewsSpider(Spider):
    name = 'news'
    start_urls = [
        'https://tushare.pro/news/news_wallstreetcn',
        'https://tushare.pro/news/news_sina',
    ]
    rotate_user_agent = True

    def parse(self, response):
        if 'login' in response.url:
            self.logger.warning('login page')
        elif response.url == 'https://tushare.pro/news/news_wallstreetcn':
            news_items_a_none = response.xpath('//div[@id="news_a-stock-channel"]/div[@class="none_class news_item"]')
            news_items_a_key = response.xpath('//div[@id="news_a-stock-channel"]/div[@class="key_news news_item"]')
            news_items_us_none = response.xpath('//div[@id="news_us-stock-channel"]/div[@class="none_class news_item"]')
            news_items_us_key = response.xpath('//div[@id="news_us-stock-channel"]/div[@class="key_news news_item"]')

            items = get_items(news_items_a_none, 'wallstreetcn_a_stock_channel', 'general', crawl_number=30)
            items.extend(get_items(news_items_a_key, 'wallstreetcn_a_stock_channel', 'key', crawl_number=10))
            items.extend(get_items(news_items_us_none, 'wallstreetcn_us_stock_channel', 'general', crawl_number=30))
            items.extend(get_items(news_items_us_key, 'wallstreetcn_us_stock_channel', 'key',  crawl_number=10))

            for item in items:
                yield item

        elif response.url == 'https://tushare.pro/news/news_sina':
            news_items_a_none = response.xpath('//div[@id="news_10"]/div[@class="none_class news_item"]')
            news_items_a_key = response.xpath('//div[@id="news_10"]/div[@class="key_news news_item"]')

            items = get_items(news_items_a_none, 'sina_news_10', 'general', crawl_number=30)
            items.extend(get_items(news_items_a_key, 'sina_news_10', 'key', crawl_number=10))

            for item in items:
                yield item
