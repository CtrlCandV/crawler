import os,json

print('欢迎使用桃花族爬虫，该脚本可以为您自动爬取桃花族的页面数据。')
print('即将开始初始化系统')
print('开始对系统第三方依赖包自检，如无相应第三方自检包，则开始自动安装')
try:
    import pymysql
except Exception:
    try:
        os.system('pip3 install pymysql')
        import pymysql
    except Exception as err:
        print('pymysql安装失败，请手动执行以下命令安装:\n pip3 install pymysql')

try:
    import requests
except Exception:
    try:
        os.system('pip3 install requests')
        import requests
    except Exception as err:
        print('requests安装失败，请手动执行以下命令安装:\n pip3 install requests')

try:
    import lxml
except Exception:
    try:
        os.system('pip3 install lxml')
        import lxml
    except Exception as err:
        print('lxml安装失败，请手动执行以下命令安装:\n pip3 install lxml')
try:
    import argparse
except Exception:
    try:
        os.system('pip3 install argparse')
        import argparse
    except Exception as err:
        print('argparse安装失败，请手动执行以下命令安装:\n pip3 install argparse')

host=input('请输入mysql数据库的地址，直接回车默认为localhost:')
if len(host)==0:
    host='localhost'
user=input('请输入mysql数据库的用户名，直接回车默认为root:')
if len(user)==0:
    user='root'
password=input('请输入mysql数据库的密码:')

print('开始尝试链接数据库，请稍等......')
try:
    db=pymysql.connect(host=host, user=user, password=password)
    print('数据库链接成功，开始检查是否存在taohua数据库')
    cursor = db.cursor()
    cursor.execute('show databases;')
    anser=cursor.fetchall()
    isOk=False
    for i in anser:
        if i[0]=='taohua':
            isOk=True
            break
    if isOk:
        print('数据库存在')
    else:
        print('数据库不存在，开始创建数据库taohua')
        cursor.execute('create database taohua;')
        print('数据库创建成功')
    print('开始进入数据库')
    cursor.execute('use taohua;')
    print('开始检查数据表是否存在')
    cursor.execute('show tables;')
    anser=cursor.fetchall()
    now=['twoList','videoData','badUrlList','badLikeList','fileMD5']
    data=[]
    for i in anser:
        if len(i)>0:
            if i[0]=='twolist':
                data.append('twoList')
            elif i[0]=='videodata':
                data.append('videoData')
            elif i[0]=='badurllist':
                data.append('badUrlList')
            elif i[0]=='badlikelist':
                data.append('badLikeList')
            elif i[0]=='fileMD5':
                data.append('fileMD5')
            data.append(i[0])
    for i in now:
        print('开始检查数据表%s是否存在'%(i))

        if i not in data:
            print('数据表%s不存在，开始创建'%(i))
            if i=='twoList':
                order='create table twoList(videoClass varchar(30) not null,id varchar(200) not null PRIMARY KEY,url varchar(200) not null,used int(1) not null)DEFAULT CHARSET=utf8;'
            elif i=='videoData':
                order='create table videoData(id varchar(200) not null PRIMARY KEY,videoClass varchar(30) not null,videoClass2 varchar(30),name varchar(500) not null,introduce TEXT,img TEXT,donload TEXT,isUsed int(1))DEFAULT CHARSET=utf8;'
            elif i=='badUrlList':
                order='create table badUrlList(url varchar(500) not null PRIMARY KEY,id varchar(200) not null,isUsed int(1) not null)DEFAULT CHARSET=utf8;'
            elif i=='fileMD5':
                order='create table fileMD5(fileWay varchar(500) not null,MD5Num varchar(200) not null PRIMARY KEY)DEFAULT CHARSET=utf8;'
            else:
                order='create table badLikeList(data varchar(500) not null PRIMARY KEY,isUsed int(1) not null)DEFAULT CHARSET=utf8;'
            cursor.execute(order)
            print('数据表%s创建成功'%(i))
        else:
            print('数据表%s存在'%(i))
    print('数据库部分成功')
except Exception as err:
    print('数据库操作失败，报错信息如下：')
    print(err)
    print('系统退出。')
    exit()
finally:
    try:
        db.close()
    except Exception:
        pass
while True:
    theBaseDir=input('请输入下载文件存放路径:')
    if len(theBaseDir)==0:
        theBaseDir='./'
    try:
        if not os.path.isdir(theBaseDir):
            os.makedirs(theBaseDir)
        break
    except Exception as err:
        print('检查目录出现错误，报错信息如下：')
        print(err)
        print('请重新输入目录')

print('开始保存基础配置信息')
data={
    'host':host,
    'user':user,
    'password':password,
    'baseDir':theBaseDir
}
try:
    f=open('config','w')
    f.write(str(json.dumps(data)))
    print('配置信息写入成功')
except Exception as err:
    print('配置信息写入失败，报错详情如下')
    print(err)
finally:
    try:
        f.close()
    except Exception as err:
        print('文件保存失败，请重新执行安装程序')
        print(err)
