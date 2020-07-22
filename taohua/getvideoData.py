import re,requests,sql,json
from lxml import etree

class getvideoData(object):
    def __init__(self,url):
        self.__sql=sql.sql()
        self.__weiNum=10
        self.__waitUrl=[]
        self.__session = requests.session()
        if url[-1]=='/':
            self.__url=url
        else:
            self.__url=url+'/'
        
        self.__xpathStr={
            '二级分类':['//h1[@class="ts"]/a/text()'],
            '名称':['//*[@id="thread_subject"]/text()'],
            '详情ID':['//td[@class="t_f"]/@id'],
            '详情':['//*[@id="%s"]/text()'],
            'img':['//*[@id="%s"]//img/@file','//div[@class="pattl"]//img/@zoomfile'],
            '下载名':['//div[@class="pattl"]//a[@target="_blank"]/text()','//td[@id="%s"]//a[@target="_blank"]/text()'],
            '下载链接':['//div[@class="pattl"]//a[@target="_blank"]/@href','//td[@id="%s"]//a[@target="_blank"]/@href']
        }
        self.__reStr={
            '':[""]
        }
        self.__badList=['jpg','png','JPG','PNG','下载附件']
    
    def setUrl(self,url):
        '''
        该函数是用来设置url参数
        '''
        if url[-1]=='/':
            self.__url=url
        else:
            self.__url=url+'/'
    def getUrl(self):
        '''
        该函数是用来返回url参数的值
        '''
        return self.__url
    
    def getWeiNum(self):
        '''
        获取单次扫描的url数目
        '''
        return self.__weiNum
    def setWeiNum(self,num):
        '''
        设置单次扫描的url数目
        '''
        try:
            now=int(num)
            if now<1:
                return (False,'数字不可小于1')
            else:
                self.__weiNum=now
                return(True,'')
        except Exception:
            return (False,'传入的不是数字')

    def __getWaitUrl(self):
        '''
        获取待读取视频url
        '''
        self.__waitUrl=self.__sql.getWaitScanUrl(self.__weiNum)
    
    def scan(self):
        '''
        进行扫描视频数据
        '''
        self.__getWaitUrl()
        while len(self.__waitUrl)>0:
            self.__getWaitUrl()
            for data in self.__waitUrl:
                try:
                    videoClass=data[0]
                    videoId=data[1]
                    videoUrl=self.__url+data[2]
                    
                    anser=self.__getPage(videoUrl)
                    html = etree.HTML(anser)
                    
                    class2Data=self.__getXpathData('二级分类',html)
                    nameData=self.__getXpathData('名称',html)
                    xiangqingID=str(self.__getXpathData('详情ID',html,isList=False))
                    xiangqing=list(self.__getXpathData('详情',html,isList=True,isPinjie=True,Pinjie=xiangqingID))
                    img=self.__getXpathData('img',html,isList=True,isPinjie=True,Pinjie=xiangqingID)
                    donloadText=self.__getXpathData('下载名',html,isList=True,isPinjie=True,Pinjie=xiangqingID)
                    donloadUrl=self.__getXpathData('下载链接',html,isList=True,isPinjie=True,Pinjie=xiangqingID)

                    donload={}
                    if len(donloadText)==len(donloadUrl):
                        for num in range(0,len(donloadUrl)):
                            donload[donloadText[num]]=donloadUrl[num]
                    elif len(donloadText)>len(donloadUrl):
                        for num in range(0,len(donloadUrl)):
                            donload[donloadText[num]]=donloadUrl[num]
                    elif len(donloadText)<len(donloadUrl):
                        for num in range(0,len(donloadUrl)):
                            if num>=len(donloadText):
                                donload['None']=donloadUrl[num]
                            else:
                                donload[donloadText[num]]=donloadUrl[num]
                    for i in list(donload.keys()):
                        now=i.split('.')
                        if len(now)==0:
                            pass
                        elif len(now)==1:
                            if i in self.__badList:
                                donload.pop(i)
                        else:
                            if now[-1] in self.__badList:
                                donload.pop(i)

                    imgList=[]
                    for iimg in img:
                        if iimg[0]=='/':
                            imgList.append(self.__url+iimg[1:])
                    img=imgList
                    
                    #(id,一级分类,二级分类,名称,介绍,str(图片链接列表),str(下载字典),1)
                    end=(self.__unicodeChange(videoId),self.__unicodeChange(videoClass),self.__unicodeChange(class2Data),self.__unicodeChange(nameData),self.__unicodeChange(json.dumps(xiangqing)),self.__unicodeChange(json.dumps(img)),self.__unicodeChange(json.dumps(donload)),1)
                    self.__sql.insertVideoData(end)
                    self.__sql.setWaitScanUrlUsed(videoId)
                except Exception as err:
                    print(err)
                    print(end)
    
    def __getXpathData(self,name,html,isList=False,isPinjie=False,Pinjie=''):
        '''
        用于获取xpath所选择的数据
        '''
        now=[]
        end=[]
        for i in self.__xpathStr[name]:
            nowi=i
            if isPinjie and '%s' in nowi:
                nowi=nowi%(Pinjie)
            now = html.xpath(nowi)
            if len(now)>0:
                if isList==False:
                    end=self.__clearStr(now[0])
                break
        if isList==False and len(now)==0:
            end=''
        if isList:
            for i in now:
                data=self.__clearStr(i.replace('\r','').replace('\n','').replace('\xa0 ','').replace('\xa0','').replace('\u3000',' '))
                if len(data)!=0 and data not in end:
                    end.append(data)
        return end


    def __getPage(self,url):
        '''
        获得页面数据
        '''
        header={
            "Host":"thzd.cc",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer":"http://thzd.cc/forum.php",
            "Connection":"keep-alive",
            "Cookie":"WMwh_2132_saltkey=Pc84lF2l; WMwh_2132_lastvisit=1593879552; Hm_lvt_acfaccaaa388521ba7e29a5e15cf85ad=1593884505,1595118229; UM_distinctid=1731aeb75224d8-0918a33cff8d2f-4c302372-190140-1731aeb75233e7; CNZZDATA1254190848=850755625-1593883578-http%253A%252F%252Ft.thzdz3.com%252F%7C1595115184; HstCfa2810755=1593884514758; HstCla2810755=1595118260228; HstCmu2810755=1593884514758; HstPn2810755=2; HstPt2810755=6; HstCnv2810755=2; HstCns2810755=2; __dtsu=104015938845196792DC0326EFAD3B81; yunsuo_session_verify=305edb3a4f52e727ccda2155f10e6e29; WMwh_2132_lastact=1595116893%09home.php%09misc; Hm_lpvt_acfaccaaa388521ba7e29a5e15cf85ad=1595118260; WMwh_2132_st_t=0%7C1595116874%7C42ec8e6dd4f17591526dd100ab5e55a1; WMwh_2132_forum_lastvisit=D_181_1595116874; WMwh_2132_secqaa=58101.59f9204b91ba3c85dc; WMwh_2132_st_p=0%7C1595116892%7C6374ba4c29ba7de925d776f430e04670; WMwh_2132_viewid=tid_2210567",
            "Upgrade-Insecure-Requests":"1",
            "Cache-Control":"max-age=0"
        }
        r=self.__session.get(url,headers=header,timeout=5,verify=False)
        return str(r.content,"utf-8")
    def __clearStr(self,data):
        '''
        清除字符串前后无意义字符
        '''
        isOk=True
        badChar=['\t','\n','\r',' ']
        while isOk:
            isOk=False
            if len(data)>0:
                if data[0] in badChar:
                    data=data[1:]
                    isOk=True
                elif data[-1] in badChar:
                    data=data[:-1]
                    isOk=True
        return data
    def __unicodeChange(self,strData):
        '''
        对字符串中的Unicode字符进行解码
        '''
        now=str(strData)
        if '\\u' in now:
            now=str(str(strData).encode('utf8').decode('unicode_escape'))
        return now
