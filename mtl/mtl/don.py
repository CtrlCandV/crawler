import urllib.request
import pymysql
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
    cursor.execute('SELECT * from photourl where don=True;')
    data = cursor.fetchone()
    try:
        if page==1:
            oldurl='https://www.meitulu.com/item/'+urlid+'.html'
        else:
            oldurl='https://www.meitulu.com/item/'+urlid+'_'+page+'.html'
        print(oldurl)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'),('Referer',oldurl)]
        urllib.request.install_opener(opener)
        imgname='./img/'+urlid+'_'+url.split('/')[-1]
        print(imgname)
        try:
            urllib.request.urlretrieve(url,filename=imgname)
        except Exception as errr:
            print(errr)
    except Exception as err:
        print(err)
conn.close()