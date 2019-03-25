# -*- coding: utf-8 -*-
import scrapy
from mtl.items import MtlItem
import re
from mtl.settings import MIN
from mtl.settings import MAX
from scrapy.http import Request

class Mtl1Spider(scrapy.Spider):
    name = 'mtl1'
    allowed_domains = ['meitulu.com']
    start_urls = ['https://www.meitulu.com/item/'+str(MIN)+'.html']

    def parse(self, response):
        item=MtlItem()
        item['url']=response.xpath("//center/img[@class='content_img']/@src").extract()
        page=int(response.xpath("//center/div[@id='pages']/a/text()").extract()[-2])
        print('page=-----------------------')
        print(page)
        num=re.compile('item/(.*?).html').findall(response.url)[0]
        if '_' in num:
            item['fid']=num.split('_')[0]
            item['pid']=num.split('_')[1]
        else:
            item['fid']=num
            item['pid']='1'
        yield item
        
        print(num)
        if '_' not in num:
            for i in range(2, page+1):
                iiurl = 'https://www.meitulu.com/item/'+num+'_'+str(i)+'.html'
                print('页码跑'+iiurl)
                yield Request(iiurl, callback=self.parse)
            if int(num)==MIN:
                for ii in range(int(num)+1,MAX+1):
                    iurl='https://www.meitulu.com/item/'+str(ii)+'.html'
                    print('大页翻'+iurl)
                    yield Request(iurl, callback=self.parse)
        

        

