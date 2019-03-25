import pymysql
import os
import time
conn = pymysql.connect(host="106.12.83.239", user="liang", passwd="Li.ng951127", db="mtl")
cursor = conn.cursor()
cursor.execute('SELECT * from photourl where don=True;')
data = cursor.fetchone()
print('data')
print(data)
while data!=None:
    urlid=data[0]
    url=data[1]
    page=data[3]
    print(urlid)
    print(url)
    print(page)
    order='update photourl set don=False where url="'+url+'";'
    print(order)
    cursor.execute(order)
    conn.commit()
    
    wgetOrder='wget -P ./img/ --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393" --referer="'
    if page==1:
        oldurl='https://www.meitulu.com/item/'+urlid+'.html'
    else:
        oldurl='https://www.meitulu.com/item/'+urlid+'_'+page+'.html'
    print(oldurl)
    wgetOrder=wgetOrder+oldurl+'" '+url
    print(wgetOrder)
    os.system(wgetOrder)
    time.sleep(0.1)
    cursor.execute('SELECT * from photourl where don=True;')
    data = cursor.fetchone()