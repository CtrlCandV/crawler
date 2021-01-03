import get2list,getvideoData,getFile,argparse,os,json

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help="输入现在的网址，如：http://www.baidu.com")
parser.add_argument('-d', '--deep', type=int, default=-1,help="确定扫描页码数，-1为全部扫描，日常扫描建议使用 10")
parser.add_argument('-c', '--config', type=str, default='config',help="输入配置文件路径（含文件名），默认为config")
parser.add_argument('-p', '--proxy', type=bool, default=False,help="是否启用代理，如启用，请配置--proxyIP和--proxyPort")
parser.add_argument('--proxyIP', type=str, default='127.0.0.1',help="输入代理地址")
parser.add_argument('--proxyPort', type=int, default=0,help="输入代理端口")
args = parser.parse_args()

print('欢迎使用某某论坛下载器，该下载器将帮助您下载种子及图片')
print('版本：V1.0')

if os.path.isfile(args.config)==False:
    print('配置文件丢失或尚未初始化，请先执行setup.py')
    exit()

try:
    f=open(args.config,mode='r')
    anser=str(f.read())
    anser=json.loads(anser)
except Exception:
    pass
finally:
    try:
        f.close()
    except Exception:
        pass

useProxy=args.proxy
if useProxy==True:
    if args.proxyPort==0:
        print("请配置--proxyIP和--proxyPort选项值，其中--proxyPort为整数，切不可为0")
        exit()
proxyIP=args.proxyIP
proxyPort=args.proxyPort
proxy=(useProxy,proxyIP,proxyPort)

print('开始扫描页面列表')
twoListClass=get2list.getTwoList(args.url,config=args.config,proxy=proxy)
twoListClass.setDeep(args.deep)
video=twoListClass.getAllClassName()
for i in video:
    print('开始获取%s页面列表'%(i))
    twoListClass.setNowJod(i)
    twoListClass.scan()
twoListClass.close()

print('开始获取视频详情')
getVideo=getvideoData.getvideoData(args.url,config=args.config,proxy=proxy)
getVideo.scan()

print('开始下载视频种子及图片')
baseDir=anser['baseDir']
if baseDir[-1]!='/' and baseDir[-1]!='\\':
    baseDir=baseDir+'/' 
baseDir=baseDir+'videoData/'

down=getFile.getFile(args.url,baseWay=baseDir,config=args.config,proxy=proxy)
down.down()

print('运行结束')
