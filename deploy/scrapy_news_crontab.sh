#!/bin/bash

PATH=$PATH:/home/ubuntu/Projects/scrapy_news/venv/bin
export PATH

cd /home/ubuntu/Projects/scrapy_news/scrapy_news
nohup scrapy crawl news >> /home/ubuntu/Projects/scrapy_news/log/scrapy_news.log &


# */30 * * * * sh /home/ubuntu/Projects/scrapy_news/deploy/scrapy_news_crontab.sh
