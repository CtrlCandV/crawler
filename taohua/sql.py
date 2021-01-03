import pymysql,json
class sql(object):
    def __init__(self,config='config'):
        try:
            f=open(config,mode='r')
            anser=str(f.read())
            anser=json.loads(anser)
        except Exception:
            pass
        finally:
            try:
                f.close()
            except Exception:
                pass
        self.__host=anser['host']
        self.__user=anser['user']
        self.__passwd=anser['password']
        self.__database='taohua'
        self.db=pymysql.connect(host=self.__host, user=self.__user, password=self.__passwd, database=self.__database)
        self.cursor = self.db.cursor()
        self.__tableList=[]
        self.flashTableList()
    
    def flashTableList(self):
        '''
        获取所有的数据表
        '''
        sqlOrder='show tables;'
        self.cursor.execute(sqlOrder)
        anser=self.cursor.fetchall()
        for tableName in anser:
            self.__tableList.append(tableName[0])
    def getTableList(self):
        return self.__tableList
    
    def uploadTwoList(self,dataList):
        '''
        上传二级列表数据

        建表语句
        create table twoList(
            videoClass varchar(30) not null,
            id varchar(200) not null PRIMARY KEY,
            url varchar(200) not null,
            used int(1) not null
        )DEFAULT CHARSET=utf8;
        '''
        insertSQL='insert into twoList (videoClass,id,url,used) values (%s,%s,%s,%s);'
        self.cursor.execute(insertSQL,dataList)
        self.db.commit()
    
    def getWaitScanUrl(self,num=10):
        '''
        获得未扫描的页面列表
        num代表单次获的页面数量
        '''
        endList=[]
        getWaitListSQL='select videoClass,id,url,used from twoList where used=1 limit 0,%s;'
        self.cursor.execute(getWaitListSQL,num)
        anser=self.cursor.fetchall()
        self.db.commit()
        for i in anser:
            endList.append(i)
        return endList
    
    def setWaitScanUrlUsed(self,videoId):
        '''
        将某个ID的页面设置为已用
        '''
        setWaitScanUrlUsedSQL='update twoList set used=0 where id=%s;'
        self.cursor.execute(setWaitScanUrlUsedSQL,str(videoId))
        self.db.commit()

    def insertVideoData(self,videoData):
        '''
        插入视频数据
        videoData格式 元组 (id,一级分类,二级分类,名称,介绍,str(图片链接列表),str(下载字典),1)

        建表语句
        create table videoData(
            id varchar(200) not null PRIMARY KEY,
            videoClass varchar(30) not null,
            videoClass2 varchar(30),
            name varchar(500) not null,
            introduce TEXT,
            img TEXT,
            donload TEXT,
            isUsed int(1)
        )DEFAULT CHARSET=utf8;
        '''
        insertVideoDataSQL='insert into videoData (id,videoClass,videoClass2,name,introduce,img,donload,isUsed) values (%s,%s,%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(insertVideoDataSQL,videoData)
        self.db.commit()

    def close(self):
        try:
            self.db.close()
        except Exception:
            pass
    
    def getWaitDownLoad(self,num=10):
        '''
        获得未下载的页面列表
        num代表单次获的页面数量
        '''
        endList=[]
        getWaitListSQL='select id,videoClass,videoClass2,name,introduce,img,donload from videoData where isUsed=1 limit 0,%s;'
        self.cursor.execute(getWaitListSQL,num)
        anser=self.cursor.fetchall()
        self.db.commit()
        for i in anser:
            endList.append(i)
        return endList
    
    def setWaitDownloadUsed(self,videoId):
        '''
        将某个ID的页面设置为已用
        '''
        setWaitScanUrlUsedSQL='update videoData set isUsed=0 where id=%s;'
        self.cursor.execute(setWaitScanUrlUsedSQL,str(videoId))
        self.db.commit()

    def getDownNum(self):
        '''
        获取已经下载的视频资料数目
        '''
        setWaitScanUrlUsedSQL='select count(*) from videoData where isUsed=0;'
        self.cursor.execute(setWaitScanUrlUsedSQL)
        try:
            anser=self.cursor.fetchall()[0][0]
            self.db.commit()
        except Exception:
            return False
        return anser
    def getAllDownNum(self):
        '''
        获取全部的视频资料数目
        '''
        setWaitScanUrlUsedSQL='select count(*) from videoData;'
        self.cursor.execute(setWaitScanUrlUsedSQL)
        try:
            anser=self.cursor.fetchall()[0][0]
            self.db.commit()
        except Exception:
            return False
        return anser
    def getAllUrlNum(self):
        '''
        获取全部的视频链接数目
        '''
        setWaitScanUrlUsedSQL='select count(*) from twoList;'
        self.cursor.execute(setWaitScanUrlUsedSQL)
        try:
            anser=self.cursor.fetchall()[0][0]
            self.db.commit()
        except Exception:
            return False
        return anser
    
    def addBadUrl(self,url,tid):
        '''
        增加下载链接黑名单
        '''
        addBadUrlOrder='insert into badUrlList (id,url,isUsed) values (%s,%s,%s);'
        error=(False,'')
        try:
            self.cursor.execute(addBadUrlOrder,(tid,url,1))
        except Exception as err:
            if "PRIMARY" not in str(err):
                error=(True,str(err))
        finally:
            try:
                self.db.commit()
            except Exception:
                pass
        return error
    
    def checkBadUrl(self,url):
        '''
        检查下载链接黑名单
        存在于黑名单，返回False，否则为True
        '''
        checkBadUrlOrder='select count(*) from badUrlList where url=%s and isUsed=1;'
        try:
            self.cursor.execute(checkBadUrlOrder,(url))
            anser=self.cursor.fetchall()[0][0]
            self.db.commit()
            anser=int(anser)
            if anser>0:
                return False
            else:
                return True
        except Exception:
            return True
    def getIdData(self,tid):
        '''
        获得某个ID的详情
        '''
        endList=[]
        getIdDataSQL='select id,videoClass,videoClass2,name,introduce,img,donload from videoData where id=%s;'
        self.cursor.execute(getIdDataSQL,tid)
        anser=self.cursor.fetchall()
        self.db.commit()
        for i in anser:
            endList.append(i)
        return endList
    def addBadLikeData(self,data):
        '''
        增加下载链接黑名单(相似列表)
        '''
        addBadLikeDataOrder='insert into badLikeList (data,isUsed) values (%s,%s);'
        error=(False,'')
        try:
            self.cursor.execute(addBadLikeDataOrder,(data,1))
        except Exception as err:
            if "PRIMARY" not in str(err):
                error=(True,str(err))
        finally:
            try:
                self.db.commit()
            except Exception:
                pass
        return error
    def getBadLikeData(self):
        '''
        获得不良类似链接
        '''
        endList=[]
        getBadDataSQL='select data from badLikeList where isUsed=1;'
        self.cursor.execute(getBadDataSQL)
        anser=self.cursor.fetchall()
        self.db.commit()
        for i in anser:
            endList.append(i[0])
        return endList
    
    def checkFileMD5(self,fileWay,MD5Num):
        """
        检查MD5值是否存在
        文件路径存在，则返回True
        文件路径不存在，MD5值不存在，返回True
        文件路径不存在，MD5值存在，返回False
        """
        #fileWayOrder="select fileWay,MD5Num from fileMD5 where fileWay=%s;"
        fileMD5Order="select fileWay,MD5Num from fileMD5 where MD5Num=%s;"
        try:
            self.cursor.execute(fileMD5Order,(MD5Num))
            anser=self.cursor.fetchall()
            self.db.commit()
            if len(anser)==0:
                return True
            else:
                for i in anser:
                    if fileWay in i:
                        return True
                return False
        except Exception as err:
            print ("数据库查询错误")
            return err

    def writeFileMD5(self,fileWay,MD5Num):
        """
        写入MD5值
        """
        writeFileMD5SQLOrder="insert into fileMD5(fileWay,MD5Num) values (%s,%s);"
        try:
            self.cursor.execute(writeFileMD5SQLOrder,(fileWay,MD5Num))
            self.db.commit()
            return True
        except Exception as err:
            if "PRIMARY" in str(err) or "primary" in str(err):
                return True
            else:
                print("MD5值写入出错："+str(err))
                return False
