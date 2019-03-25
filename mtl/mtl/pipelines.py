# -*- coding: utf-8 -*-
import pymysql
from mtl.passwd import passwd
#from scrapy.http import request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MtlPipeline(object):
    def process_item(self, item, spider):
        user=passwd()
        conn = pymysql.connect(host=user.getHost(), user=user.getUser(), passwd=user.getpasswd(), db="mtl")
        for i in item["url"]:
            data="insert into photourl (urlid,url,don,page) values('"+item['fid']+"','"+i+"',"+'True,"'+item['pid']+'");'
            conn.query(data)
            conn.commit()
        conn.close()
        return item
