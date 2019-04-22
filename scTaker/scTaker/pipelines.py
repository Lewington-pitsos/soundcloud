# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scTaker.settings import FILES_STORE
from subprocess import call

default_extension = '.m3u8'

class TrackPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta["title"] + default_extension
    
    def get_media_requests(self, item, info):
        file_url = item['file_url']
        request = scrapy.Request(url=file_url)
        request.meta['title'] = item['title']
        return request

    def item_completed(self, results, item, info):
        print("finished <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(item['title'])
        file_path = FILES_STORE + "/" + item['title']
        print(file_path)
        call([
            "ffmpeg",
            "-i", 
            file_path + default_extension,
            "-acodec", 
            "copy",
            file_path + ".mp3"
        ])

        if isinstance(item, dict) or self.files_result_field in item.fields:
            item[self.files_result_field] = [x for ok, x in results if ok]
        return item
