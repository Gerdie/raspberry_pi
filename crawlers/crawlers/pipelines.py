# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class AttributionPipeline(object):
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        # Finish with attribution
        with open(spider.filename, 'a+') as f:
            f.write(spider.attribution + '\n')
