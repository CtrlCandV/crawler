import sql,os,json,hashlib

class getFile(object):
    def __init__(self,url,baseWay='./videoData/',config='config',proxy=(False,'127.0.0.1',0)):
        if url[-1]=='/':
            self.__url=url
        else:
            self.__url=url+'/'
        self.host=self.__url.replace('http://','').replace('https://','').split('/')[0]
        self.header=[
            "Host: "+self.host,
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept: */*",
            "Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection: keep-alive",
            "Referer: http://"+self.host+"/forum.php"
        ]
        if baseWay[-1]=='/':
            self.__baseWay=baseWay
        else:
            self.__baseWay=baseWay+'/'
        
        self.__fileName='介绍.txt'

        self.__proxy=proxy
        self.__proxyDict={
            "http":"http://"+self.__proxy[1]+':'+str(self.__proxy[2])+'/',
            "https":"https://"+self.__proxy[1]+':'+str(self.__proxy[2])+'/',
        }

        self.__waitData=[]
        self.__weiNum=10

        self.__sql=sql.sql(config=config)
    
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
    def setBaseWay(self,baseWay):
        '''
        该函数是用来设置url参数
        '''
        if baseWay[-1]=='/':
            self.__baseWay=baseWay
        else:
            self.__baseWay=baseWay+'/'
    def getBaseWay(self):
        '''
        该函数是用来返回url参数的值
        '''
        return self.__baseWay
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



    def __getWaitData(self):
        '''
        获取待读取视频url
        '''
        self.__waitData=self.__sql.getWaitDownLoad(self.__weiNum)

    def down(self):
        '''
        开始下载
        '''
        self.__getWaitData()
        while len(self.__waitData)>0:
            self.__getWaitData()
            try:
                for data in self.__waitData:
                    try:
                        img=self.__getImgList(data)
                        down=self.__getDownLoad(data)
                        if len(img)>0 or len(down)>0:
                            way=self.__getDirWay(data)
                            self.__createDir(way)
                            fileData=self.__getFileData(data)
                            fileWay=self.__addDirWay(way,self.__fileName,isFile=True)
                            self.__writeFileData(fileData,fileWay)
                            self.__downImg(img,way)
                            self.__downTorr(down,way)
                        self.__sql.setWaitDownloadUsed(data[0])
                    except Exception as ierr:
                        print(str(data[0])+'发生错误'+str(ierr))
            except Exception as err:
                print('下载大循环错误'+str(err))

    def __createDir(self,way):
        '''
        若目录不存在，则创建目录
        '''
        if not os.path.isdir(way):
            os.makedirs(way)
    
    def __getDirWay(self,data):
        '''
        传入数据库返回元组，生成存放目录
        id,videoClass,videoClass2,name,introduce,img,donload
        '''
        way=self.__baseWay
        way=self.__addDirWay(way,data[1])
        way=self.__addDirWay(way,data[2])
        way=self.__addDirWay(way,data[0])
        return way

    def __addDirWay(self,nowway,addData,isFile=False):
        '''
        在现有目录后，增加一级目录或文件
        '''
        way=nowway
        if way[-1]!='/' and way[-1]!='\\':
            way=way+'/'
        way=way+addData
        if isFile:
            if way[-1]=='/' or way[-1]=='\\':
                way=way[:-1]
        else:
            if way[-1]!='/' and way[-1]!='\\':
                way=way+'/'
        return way
        
    def __getFileData(self,data):
        '''
        传入数据库返回元组，生成介绍文件内容
        id 0,videoClass 1,videoClass2 2,name 3,introduce 4,img 5,donload 6
        
        '''
        fileData='影片名称：'+data[3]+'\n'
        try:
            introduce=json.loads(data[4])
        except Exception:
            introduce=str(data[4])
        if type(introduce)==type([]):
            for i in introduce:
                fileData=fileData+str(i)+'\n'
        else:
            fileData=fileData+str(introduce)+'\n'
        fileData=fileData[:-1]
        return fileData
    def __writeFileData(self,data,way):
        '''
        将数据写入文件
        '''
        try:
            f=open(way,mode='w')
            f.write(data)
        except Exception as err:
            print('文件写入错误'+str(err))
        finally:
            try:
                f.close()
            except Exception:
                pass

    def __getImgList(self,data):
        '''
        将传入的data数据，转化成img的列表
        id 0,videoClass 1,videoClass2 2,name 3,introduce 4,img 5,donload 6
        '''
        img=json.loads(data[5])
        return list(img)
    def __getDownLoad(self,data):
        '''
        将传入的data数据，转化成种子的字典
        id 0,videoClass 1,videoClass2 2,name 3,introduce 4,img 5,donload 6
        '''
        down=json.loads(data[6])
        return dict(down)
    def __downTorr(self,down,way):
        '''
        下载种子文件
        '''
        fileName=list(down.keys())
        url='http://'+str(self.host)+'/forum.php?mod=attachment&aid=%s'
        if self.__proxy[0]==False:
            order='wget --timeout=10 --tries=3 -q "%s" -O "%s"'
        else:
            order='wget -e "http_proxy='+str(self.__proxyDict["http"])+'" --timeout=10 --tries=3 -q "%s" -O "%s"'

        for name in fileName:
            try:
                if 'torr' not in name and 'TORR' not in name:
                    continue
                fileId=down[name].split('=')[-1]
                nowUrl=url%(fileId)
                fileWay=self.__addDirWay(way,name,isFile=True)
                nowOrder=order%(nowUrl,fileWay)
                for i in range(0,3):
                    os.popen(nowOrder).read()
                    if self.__checkFileNull(fileWay):
                        
                        md5Check=self.__checkFileExist(fileWay)
                        if md5Check==False:
                            try:
                                os.remove(fileWay)
                            except Exception:
                                pass
                        break
                    else:
                        try:
                            os.remove(fileWay)
                        except Exception:
                            pass
            except Exception as err:
                print('下载种子文件错误'+str(err))
    def __downImg(self,imgList,way):
        '''
        下载图片
        '''
        if self.__proxy[0]==False:
            order='wget --timeout=10 --tries=3 -q "%s" -O "%s"'
        else:
            order='wget -e "http_proxy='+str(self.__proxyDict["http"])+'" --timeout=30 --tries=3 -q "%s" -O "%s"'
        num=0
        for img in imgList:
            try:
                num=num+1
                if img.split('.')[-1]=='gif' or img.split('.')[-1]=='GIF':
                    fileName=str(num)+'.gif'
                else:
                    fileName=str(num)+'.jpg'
                fileWay=self.__addDirWay(way,fileName,isFile=True)
                nowOrder=order%(img,fileWay)
                for i in range(0,3):
                    os.popen(nowOrder).read()
                    if self.__checkFileNull(fileWay):
                        md5Check=self.__checkFileExist(fileWay)
                        if md5Check==False:
                            try:
                                os.remove(fileWay)
                            except Exception:
                                pass
                        break
                    else:
                        try:
                            os.remove(fileWay)
                        except Exception:
                            pass
            except Exception as err:
                print('下载图片错误'+str(err))
    
    def __checkFileNull(self,fileWay):
        """
        检查是否为空文件
        """
        try:
            if os.path.getsize(fileWay)==0:
                return False
            else:
                return True
        except Exception:
            return False
    
    def __checkFileExist(self,fileWay):
        """
        检查文件MD5值是否已经存在
        """
        md5Str=self.__get_md5_value(fileWay)
        anser=self.__sql.checkFileMD5(fileWay,md5Str)
        if anser==True:
            self.__sql.writeFileMD5(fileWay,md5Str)
            return True
        else:
            return False

    
    def __get_md5_value(self,filename):
        md5 = ""
        with open(filename, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
        return str(md5)
