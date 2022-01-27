# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class TextPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            item["title"] = clean_spaces(item["title"])
            return item
        else:
            raise DropItem("Missing title in %s" % item)




    def modif_spe(string):
        #new_string = unicodedata.normalize('NFKD',string).encode('ascii','ignore')
        new_string = unidecode(string)
        return new_string
    
def clean_spaces(string):
    if string:
        return " ".join(string.split())