# -*- coding: utf-8 -*-
import urllib.request
import re
import pymysql
from lxml import etree
import time
data=urllib.request.urlopen("https://gugong.228.com.cn/").read().decode("utf-8","ignore").replace('\r','').replace('\n','').replace('\t','').replace('<b>','').replace('</b>','')
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="1", db="other")
html = etree.HTML(data)
html_data = html.xpath('//ul[@class="date_talo"]/li/text()')
anser=[]
for i in html_data:
    anser.append(str(i).replace(' ',''))

for i in anser:
    order='insert into gg (fdate,ftime,tdate,num) values ("'
    tmon=i.split('月')
    tday=tmon[1].split('日')
    ii=tday[1]
    tmon=tmon[0]
    tday=tday[0]
    if '余' in ii:
        ii=ii.replace('余','').replace('人','').replace(' ','')
        num=-2
        try:
            num=int(ii)
        except Exception as err:
            print(err)
    else:
        num=-1
    if len(tmon)==1:
        tmon='0'+tmon
    if len(tday)==1:
        tday='0'+tday
    tdate=tmon+tday
    fday=str(time.strftime('%m%d',time.localtime(time.time())))
    ftime=str(time.strftime('%H%M',time.localtime(time.time())))
    order=order+fday+'","'+ftime+'","'+tdate+'",'+str(num)+');'
    print(i)
    print(order)
    conn.query(order)
    conn.commit()
conn.close()


