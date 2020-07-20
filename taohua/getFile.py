import sql,os,json

class getFile(object):
    def __init__(self,url,baseWay='./videoData/'):
        self.header=[
            "Host: thzd.cc",
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept: */*",
            "Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection: keep-alive",
            "Referer: http://thzd.cc/thread-2210542-1-1.html",
            "Cookie: WMwh_2132_saltkey=Pc84lF2l; WMwh_2132_lastvisit=1593879552; Hm_lvt_acfaccaaa388521ba7e29a5e15cf85ad=1593884505,1595118229; UM_distinctid=1731aeb75224d8-0918a33cff8d2f-4c302372-190140-1731aeb75233e7; CNZZDATA1254190848=850755625-1593883578-http%253A%252F%252Ft.thzdz3.com%252F%7C1595136784; HstCfa2810755=1593884514758; HstCla2810755=1595137337255; HstCmu2810755=1593884514758; HstPn2810755=6; HstPt2810755=15; HstCnv2810755=5; HstCns2810755=7; __dtsu=104015938845196792DC0326EFAD3B81; yunsuo_session_verify=374de42a941f4021e9425d6c4481a451; WMwh_2132_lastact=1595135970%09home.php%09misc; Hm_lpvt_acfaccaaa388521ba7e29a5e15cf85ad=1595137336; WMwh_2132_st_t=0%7C1595135276%7C2b676ce3aac1724b687b5e5a8ec429d2; WMwh_2132_forum_lastvisit=D_181_1595134940D_182_1595135276; WMwh_2132_secqaa=169413.86b1adf16d34cbe219; WMwh_2132_st_p=0%7C1595135968%7C11ad8111c91c877b32822a8303d520af; WMwh_2132_viewid=tid_1000004"
        ]
        if url[-1]=='/':
            self.__url=url
        else:
            self.__url=url+'/'
        if baseWay[-1]=='/':
            self.__baseWay=baseWay
        else:
            self.__baseWay=baseWay+'/'
        
        self.__fileName='介绍.txt'

        self.__waitData=[]
        self.__weiNum=10

        self.__sql=sql.sql()
    
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
                        way=self.__getDirWay(data)
                        self.__createDir(way)
                        fileData=self.__getFileData(data)
                        fileWay=self.__addDirWay(way,self.__fileName,isFile=True)
                        self.__writeFileData(fileData,fileWay)
                        img=self.__getImgList(data)
                        down=self.__getDownLoad(data)
                        self.__downImg(img,way)
                        self.__downTorr(down,way)
                        self.__sql.setWaitDownloadUsed(data[0])
                    except Exception as ierr:
                        print(str(data[0])+str(ierr))
            except Exception as err:
                print(err)

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
        introduce=json.loads(data[4])
        for i in introduce:
            fileData=fileData+str(i)+'\n'
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
            print(err)
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
        将传入的data数据，转化成img的列表
        id 0,videoClass 1,videoClass2 2,name 3,introduce 4,img 5,donload 6
        '''
        down=json.loads(data[6])
        return dict(down)
    def __downTorr(self,down,way):
        '''
        下载种子文件
        '''
        fileName=list(down.keys())
        url='http://thzd.cc/forum.php?mod=attachment&aid=%s'
        order='wget "%s" -O "%s"'
        for name in fileName:
            try:
                fileId=down[name].split('=')[-1]
                nowUrl=url%(fileId)
                fileWay=self.__addDirWay(way,name,isFile=True)
                nowOrder=order%(nowUrl,fileWay)
                a=os.popen(nowOrder).read()
            except Exception as err:
                print(err)
    def __downImg(self,imgList,way):
        '''
        下载图片
        '''
        order='wget "%s" -O "%s"'
        num=0
        for img in imgList:
            try:
                num=num+1
                fileName=str(num)+'.jpg'
                fileWay=self.__addDirWay(way,fileName,isFile=True)
                nowOrder=order%(img,fileWay)
                a=os.popen(nowOrder).read()
            except Exception as err:
                print(err)