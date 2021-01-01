import sql,time,argparse,os

def getDir(fileWay):
    '''
    获得路径切分的数值
    '''
    now =str(fileWay)
    num=len(now)
    while num>0:
        num=num-1
        if now[num]=='/' or now[num]=='\\':
            return num+1
    return False

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileWay', type=str, default='./index.html',help="输入输出文件的地址，含文件名，文件后缀为html")
parser.add_argument('-t', '--time', type=int, default=60,help="每隔多长时间刷新一次，单位 秒，建议60秒一次。")
parser.add_argument('-c', '--config', type=str, default='config',help="输入配置文件路径（含文件名），默认为config")
args = parser.parse_args()

print('欢迎使用进度展示器，该展示器将自动查询数据库，生成web页面，供您查阅')
print('版本：V1.0')

try:
    timeNum=int(args.time)
    if timeNum<=0:
        print('时间输入不合法，请输入大于0的时间，程序退出')
        exit()
except Exception:
    print('时间输入不合法，程序退出')
    exit()

try:
    way=str(args.fileWay)
    try:
        if way[-5:]=='.html':
            dirWayNum=getDir(way)
        else:
            dirWayNum=-1
    except Exception:
        dirWayNum=-1
except Exception as err:
    print('文件路径输入不合法，程序退出')
    print(err)
    exit()
if dirWayNum==-1:
    fileName='index.html'
    dirWay=way
    if dirWay[-1]!='/' and dirWay[-1]!='\\':
        dirWay=dirWay+'/'
elif dirWayNum==False:
    fileName=way
    dirWay='./'
else:
    fileName=way[dirWayNum:]
    dirWay=way[:dirWayNum]
try:
    if os.path.exists(dirWay)==False:
        os.makedirs(dirWay)
except Exception as err:
    print('文件路径输入不合法，程序退出')
    print(err)
    exit()

fileWay=dirWay+fileName


try:
    while True:
        try:
            a=sql.sql(args.config)
            allNum=a.getAllDownNum()
            downNum=a.getDownNum()
            allUrlNum=a.getAllUrlNum()
            UrlPoint=float(allNum)/float(allUrlNum)
            UrlPoint=UrlPoint*100
            downPoint=float(downNum)/float(allNum)
            downPoint=downPoint*100

            timeStr=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            f=open(fileWay,mode='w')
            word="""
            <html>\n
                <title>艺术获取系统进度</title>\n
                    <h1 align="center">
                        <font face="verdana">整体进展</font>
                    </h1>\n
                    <p align="center">
                        <font face="verdana">获取链接数:%s</font>
                    </p>\n
                    <p align="center">
                        <font face="verdana">解析链接数:%s</font>
                    </p>\n
                    <p align="center">
                        <font face="verdana">完成下载数:%s</font>
                    </p>\n
                    <p align="center">
                        <font face="verdana" color="blue">解析进度:%s%%</font>
                    </p>\n
                    <p align="center">
                        <font face="verdana"  color="red">下载进度:%s%%</font>
                    </p>\n
                    <p align="center">
                        <font face="verdana"  color="#ADADAD" size=2>数据采集时间:%s</font>
                    </p>\n
            </html>"""
            f.write(word%(allUrlNum,allNum,downNum,UrlPoint,downPoint,timeStr))
        except Exception as ierr:
            print(ierr)
        finally:
            try:
                f.close()
            except Exception:
                pass
            try:
                a.close()
            except Exception:
                pass
            time.sleep(timeNum)
except Exception as err:
    print(err)
