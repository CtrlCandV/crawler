import pymysql,json
class sql(object):
    def __init__(self):
        try:
            f=open('config',mode='r')
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
        except Exception:
            return False
        return anser
