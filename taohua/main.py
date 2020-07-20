import get2list,getvideoData,getFile,argparse,os,json

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help="输入现在的网址，如：http://www.baidu.com")
parser.add_argument('-d', '--deep', type=int, default=-1,help="确定扫描页码数，-1为全部扫描，日常扫描建议使用 10")
args = parser.parse_args()

print('欢迎使用某某论坛下载器，该下载器将帮助您下载种子及图片')
print('版本：V1.0')

if os.path.isfile('config')==False:
    print('配置文件丢失或尚未初始化，请先执行setup.py')
    exit()

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

print('开始扫描页面列表')
twoListClass=get2list.getTwoList(args.url)
twoListClass.setDeep(args.deep)
video=twoListClass.getAllClassName()
for i in video:
    print('开始获取%s页面列表'%(i))
    twoListClass.setNowJod(i)
    twoListClass.scan()
twoListClass.close()

print('开始获取视频详情')
getVideo=getvideoData.getvideoData(args.url)
getVideo.scan()

print('开始下载视频种子及图片')
baseDir=anser['baseDir']
if baseDir[-1]!='/' and baseDir[-1]!='\\':
    baseDir=baseDir+'/' 
baseDir=baseDir+'videoData/'

down=getFile.getFile(args.url,baseWay=baseDir)
down.down()

print('运行结束')