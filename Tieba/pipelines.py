# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem


class KeyWordsPipeline(object):
    def process_item(self, item, spider):
        if item is None or self.match(item) == 0:
            raise DropItem()
        else:
            return item

    @staticmethod
    def match(item):
        matched = 0
        if item["title"] is not None:
            match_words = ["地址", "电话", "手机", "位置", "联系", "在那", "哪"]
            for word in match_words:
                if item["title"].find(word) > 0:
                    matched = 1
                    break

        return matched


class SavePipeline(object):

    def __init__(self):
        self.files = {}

    def process_item(self, item, spider):
        category = item["category"]
        print(category)
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        if category not in self.files:
            self.files[category] = open(category + '.json', 'w', encoding="utf-8")
        self.files[category].write(line)
        return item
