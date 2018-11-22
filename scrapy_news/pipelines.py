# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import pymysql


class MySQLPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='scrapy_tutorial',
            user='root',
            passwd='mysql123456',
            charset='utf8',
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            sql_command = 'insert ignore into news (content, category, resource, publish_datetime, timestamp) values (%s, %s, %s, %s, %s)'
            item_values = (item['content'], item['category'], item['resource'], item['publish_datetime'], item['timestamp'])
            self.cursor.execute(sql_command, item_values)
            logging.info('insert news succeed')
        except Exception as exception:
            self.connection.rollback()
            logging.warning(exception)
        self.connection.commit()

        return item
