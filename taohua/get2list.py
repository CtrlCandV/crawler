import re,requests,sql,os
from lxml import etree

class getTwoList(object):
    def __init__(self,url,config='config',proxy=(False,'127.0.0.1',0)):
        '''
        该class是为了获取二级下的列表详情
        如 亚洲无码、欧美无码下有哪些页面
        '''
        self.__webList={
            '亚洲无码':'forum-181-%s.html',
            '亚洲有码':'forum-220-%s.html',
            '欧美无码':'forum-182-%s.html',
            '国内原创':'forum-69-%s.html',
            '三级电影':'forum-73-%s.html',
            '蓝光原盘':'forum-177-%s.html',
            '资源合集':'forum-203-%s.html',
            '热门电影':'forum-196-%s.html',
            '性爱自拍图片':'forum-42-%s.html',
            '美图写真':'forum-137-%s.html',
            '人体艺术图片':'forum-56-%s.html',
            '街头抓拍':'forum-57-%s.html',
            '欧美图片':'forum-221-%s.html',
            'AV美图':'forum-239-%s.html',
            '动态图区':'forum-200-%s.html',
            '漫画':'forum-307-%s.html'
        }

        if url[-1]=='/':
            self.__url=url
        else:
            self.__url=url+'/'
        
        self.__proxy=proxy
        self.__proxyDict={
            "http":"http://"+self.__proxy[1]+':'+str(self.__proxy[2])+'/',
            "https":"https://"+self.__proxy[1]+':'+str(self.__proxy[2])+'/',
        }

        self.host=self.__url.replace('http://','').replace('https://','').split('/')[0]
        self.__nowJod=list(self.__webList.keys())[0]
        self.__nowJodUrl=self.__url+self.__webList[self.__nowJod]
        self.__deep=-1
        self.__session = requests.session()
        self.__sql=sql.sql(config=config)
        
    def getAllClassName(self):
        '''
        获取所有影片二级名称
        '''
        return list(self.__webList.keys())

    def getNowJod(self):
        '''
        返回当前执行的任务名称
        '''
        return self.__nowJod

    def setNowJod(self,name='',num=-1):
        '''
        设置当前的任务名称。
        可以选择传入名称或数字编号，编号从0开始。
        若传入编号，则以编号为准，若无编号，则以name为准
        返回：（True/False,str）
        '''
        nowList=self.getAllClassName()
        if num>=0:
            if num>=len(nowList):
                return (False,'数字超出待选列表长度')
            else:
                try:
                    self.__nowJod=nowList[num]
                    self.__nowJodUrl=self.__url+self.__webList[nowList[num]]
                    return (True,'')
                except Exception as err:
                    return (False,str(err))
        else:
            if name in nowList:
                try:
                    self.__nowJod=name
                    self.__nowJodUrl=self.__url+self.__webList[name]
                    return (True,'')
                except Exception as err:
                    return (False,str(err))
            else:
                return (False,'没有您想要的分类')

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

    def getDeep(self):
        '''
        返回扫描深度
        如果为-1 则为全部扫描，否则为几则扫描几页
        '''
        return self.__deep
    def setDeep(self,num):
        '''
        设置扫描深度
        -1为全部扫描，其它数字则对应扫描页数
        返回：（True/False,str）
        '''
        try:
            inum=int(num)
        except Exception:
            return (False,'请输入整数')
        self.__deep=inum
        return(True,'')
    
    def scan(self):
        '''
        开始扫描
        '''
        anser=self.__getPage(1)
        getEndPageNumPath='<a href="forum-[0-9]*?-([0-9]*?).html"'
        listXpath=['/html/body/div[7]/div[4]/div/div/div[4]/div[2]/form/table/tbody/tr/th/a[2]/@href','/html/body/div[7]/div[4]/div/div/div[4]/div[2]/form/ul/li/h3/a/@href']
        endPageNum=re.findall(getEndPageNumPath,anser)
        endPageNum=self.__getBigNum(endPageNum)
        if endPageNum==False:
            return False
        else:
            if self.__deep==-1:
                self.__deep=endPageNum
            else:
                if self.__deep>endPageNum:
                    self.__deep=endPageNum
        for num in range(1,self.__deep+1):
            try:
                error=(False,'')
                anser=self.__getPage(num)
                html = etree.HTML(anser)
                for listXpathNow in listXpath:
                    html_data = html.xpath(listXpathNow)
                    if len(list(html_data))==0:
                        continue
                    for pageUrl in html_data:
                        try:
                            now=str(pageUrl)
                            if 'javascript' not in now and 'None' not in now:
                                sqlData=(self.__nowJod,now.split('-')[1],now,1)
                                try:
                                    self.__sql.uploadTwoList(sqlData)
                                except Exception as err:
                                    if "PRIMARY" not in str(err):
                                        error=(True,str(err))
                        except Exception as err:
                            error=(True,str(err))
                    break
            except Exception as err:
                error=(True,str(err))
            if error[0] :
                print('存在错误，样例：'+error[-1])
    def close(self):
        self.__sql.close()
    
    def __getPage(self,num):
        '''
        获得页面数据
        '''
        header={
            "Host":self.host,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer":"http://"+self.host+"/forum.php",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "Cache-Control":"max-age=0"
        }
        url=self.__nowJodUrl%(str(num))
        if self.__proxy[0]==False:
            r=self.__session.get(url,headers=header,timeout=15,verify=False)
        else:
            r=self.__session.get(url,headers=header,timeout=15,verify=False,proxies=self.__proxyDict)
        return str(r.content,"utf-8")
    def __getBigNum(self,numList):
        '''
        获得最大的数字
        '''
        bigNum=[]
        for i in numList:
            try:
                num=int(i)
                if len(bigNum)==0:
                    bigNum=[num]
                else:
                    if num>bigNum[0]:
                        bigNum=[num]
            except Exception:
                pass
        if len(bigNum)>0:
            return bigNum[0]
        else:
            return False
