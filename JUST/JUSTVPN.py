import urllib.request
import http.cookiejar
import random
import time
import re
import ssl
import qrcode
ssl._create_default_https_context = ssl._create_unverified_context

print('程序启动........')
print('江苏科技大学学子可以使用本程序免费下载知网的PDF文件。')
print('程序版本号：V1.1\n开发者:无名\n声明：\n本程序为开源项目，绝不盗取任何用户信息，详细代码请访问下面的链接查看')
print('网址：https://github.com/CtrlCandV/crawler/tree/master/JUST')
print("本程序的开发与使用不触犯任何法律规定\n本程序的开发与使用不危害任何组织和个人的网络安全\n本程序的开发与使用不侵犯任何组织和个人的版权与合法权益")
print('详细法律声明与程序行为描述请见上述网址。')
print('对于恶意侵犯本程序与本人的名誉权的行为，编纂谣言抹黑程序行为的行为，本人依法保留追诉的权利。')
print('恶意篡改本程序，进行危害网络与用户安全的行为，依法保留追诉的权利，且造成的损失由篡改者承担。')
print('本程序欢迎同学改进，但是请标明出处，改进所造成的安全问题，由改进人承担，且不得用于商用。')
print('商用本程序或部分源码需获得书面授权，未经授权私自以引用、抄袭等行为商用的，依法保留追诉的权利。')
print('出售本程序及个人学号密码是违法行为，所造成的任何处罚与损失，由出售者承担。')
print('如您同意以上条款，可继续使用本程序，否则请退出。')
print('程序使用教程也可以访问上述网址查看。\n')

user=str(input('请输入学号：'))
passwd=str(input('请输入密码（默认为身份证号后六位）:'))

#启动cookie
print('启动cookie与浏览器标识。')
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
opener.addheaders=[
("Referer","https://vpn.just.edu.cn/"),
('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'),
('Accept-Language', 'zh-CN'),
('Content-Type','application/x-www-form-urlencoded'),
('Accept-Encoding','gzip, deflate'),
('Host','vpn.just.edu.cn'),
('Connection','Keep-Alive'),
('Cache-Control','no-cache')
]
urllib.request.install_opener(opener)
try:
    #先打开一次主页
    print('开始打开主页')
    url='https://vpn.just.edu.cn/'
    urllib.request.urlopen(url)

    #传输用户名密码
    print('向学校VPN服务器传输学号和密码')
    url="https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi"
    postdata =urllib.parse.urlencode({
    'tz_offset':'480',
    'username':user,
    'password':passwd,
    'realm':'LDAP-REALM',
    'btnSubmit':urllib.request.quote('登录')
    }).encode('utf-8')
    req = urllib.request.Request(url,postdata)
    req=urllib.request.urlopen(req)
    requrl=req.geturl()
    reqdata=req.read().decode("utf-8","ignore")
    if 'welcome.cgi?p=user-confirm' in requrl:
        print('您已在其他浏览器登录，即将帮您退出。')
        pat_logagin='name="FormDataStr" value="(.*?)">'
        logagin=str(re.compile(pat_logagin,re.S).findall(reqdata)[0])
        print('成功获取FormDataStr值，开始构建继续会话请求')
        url='https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi'
        postdata =urllib.parse.urlencode({
            'btnContinue':urllib.request.quote('继续会话'),
            'FormDataStr':logagin}).encode('utf-8')
        req= urllib.request.Request(url,postdata)
        req=urllib.request.urlopen(req)
        print('继续会话成功。')
    elif 'welcome.cgi?p=failed' in requrl:
        print('学号或密码输入错误，程序退出。')
        raise Exception("学号或密码错误")

    try:
        #发送检查yes信息，并获取xsauth信息
        print('发送check信息，获取xsauth信息。')
        url2='https://vpn.just.edu.cn/dana/home/starter0.cgi?check=yes'
        thevalue1=urllib.request.urlopen(url2).read().decode("utf-8","ignore")
        pat_value1='<input id="xsauth_404" type="hidden" name="xsauth" value="(.*?)">'
        value1=str(re.compile(pat_value1,re.S).findall(thevalue1)[0])
        print('获取xsauth信息成功，信息为：'+value1)
    except Exception as erro:
        print('未知错误：'+str(erro))
        raise Exception("check错误")

    print('访问blank网页')
    url3='https://vpn.just.edu.cn/dana-na/html/blank.html'
    urllib.request.urlopen(url3).read().decode("utf-8","ignore")

    print('传输xsauth信息与时间戳。')
    url4='https://vpn.just.edu.cn/dana/home/starter0.cgi'
    post2=urllib.parse.urlencode({
    'xsauth':value1,
    'tz_offset':'480',
    'clienttime':str(int(time.time())),
    'url':'',	
    'activex_enabled':'1',
    'java_enabled':'0',
    'power_user':'0',
    'grab':'1',
    'browserproxy':'',
    'browsertype':'',
    'browserproxysettings':'',
    'check':'yes'
    }).encode('utf-8')
    req2 = urllib.request.Request(url4,post2)
    urllib.request.urlopen(req2)

    print('打开starter网页。')
    url5='https://vpn.just.edu.cn/dana/home/starter.cgi'
    urllib.request.urlopen(url5).read().decode("utf-8","ignore")

    print('进入个人主页')
    url6='https://vpn.just.edu.cn/dana/home/index.cgi'
    data6=urllib.request.urlopen(url6).read().decode("utf-8","ignore")
    pat_value6='<title>(.*?)</title>'
    value6=str(re.compile(pat_value6,re.S).findall(data6)[0])

    print('获取知网链接时，请保证在知网是未登录状态')
    openurl=str(input("请输入知网链接（命令行界面中鼠标右键为粘贴）:")).split('://')[1]
    print('开始构建请求地址.......')
    url='https://vpn.just.edu.cn/'
    openurl=openurl.split('/')
    for i in openurl[1:-1]:
        url=url+i+'/'
    url=url+',DanaInfo='+openurl[0]+'+'+openurl[-1]
    print('请求地址构建成功，请求地址为：'+url)
    print('开始访问该网页')
    data7=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat7='name="pdfDown" href="(.*?)"'
    try:
        value7=str(re.compile(pat7,re.S).findall(data7)[0]).split('&amp;')
    except Exception as err:
        print('错误.............')
        print('无法获取PDF链接，该文章不存在PDF文件或者是网址错误')
        print('网址必须为文章的详情页，而非内容浏览页。')
        raise Exception("PDF下载链接解析异常。")

    print('访问成功，开始构建下载链接')
    url='https://vpn.just.edu.cn'+value7[0]
    for i in value7[1:-1]:
        url=url+'&'+i
    url=url+'&'+value7[-1].split('&')[0]
    print('下载链接构建成功，下载链接为：'+url)

    patName='<title>(.*?)</title>'
    print('开始获取标题......')
    name=str(re.compile(patName,re.S).findall(data7)[0]).replace('\t','').replace('\n','').replace('\r','').replace(' ','').replace('-中国知网','').replace('/','')
    name=name.replace('\\','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','')
    print('标题获取成功，标题为：'+name)

    localfile="./"+name+".pdf"
    print('开始下载文件')
    print('存在低概率的下载好的文件损坏的可能，可以尝试重新下载。若多次仍然损坏，可能是知网存储的文件就是损坏的。\n')
    urllib.request.urlretrieve(url,filename=localfile)
    print('文件下载成功，文件保存在该程序所在的目录下。')
except Exception as err:
    print(err)
    print('\n\n遇到错误请访问https://github.com/CtrlCandV/crawler/tree/master/JUST，确认最新版是否解决该问题。\n\n')
finally:
    print('开始退出登录。')
    url='https://vpn.just.edu.cn/dana-na/auth/logout.cgi'
    logout=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat_out='<title>(.*?)</title>'
    logoutVal=str(re.compile(pat_out,re.S).findall(logout)[0])
    if 'Logout' in logoutVal:
        print('退出成功。\n\n')
    else:
        print('退出失败。\n\n')
    print('power by 无名 zsl_email@qq.com')
    end=input('直接回车退出，输入1支付宝资助我，输入2微信资助我:\n\n')
    if end=='1':
        img = qrcode.make("https://render.alipay.com/p/s/i?scheme=%61%6C%69%70%61%79%73%3A%2F%2F%70%6C%61%74%66%6F%72%6D%61%70%69%2F%73%74%61%72%74%61%70%70%3F%73%61%49%64%3D%31%30%30%30%30%30%30%37%26%71%72%63%6F%64%65%3D%25%34%38%25%35%34%25%35%34%25%35%30%25%35%33%25%33%41%25%32%46%25%32%46%25%35%31%25%35%32%25%32%45%25%34%31%25%34%43%25%34%39%25%35%30%25%34%31%25%35%39%25%32%45%25%34%33%25%34%46%25%34%44%25%32%46%25%34%36%25%34%42%25%35%38%25%33%30%25%33%38%25%33%37%25%33%33%25%33%36%25%34%38%25%33%38%25%35%35%25%35%34%25%35%35%25%34%44%25%34%42%25%34%34%25%34%43%25%34%46%25%34%38%25%35%34%25%33%33%25%34%32%25%33%46%25%35%46%25%37%33%25%33%44%25%37%37%25%36%35%25%36%32%25%32%44%25%36%46%25%37%34%25%36%38%25%36%35%25%37%32")
        img.get_image().show()
    elif end=='2':
        img = qrcode.make("wxp://f2f0GA69ywUnHUTYXv4GngBHn6BVlOwYs5gD")
        img.get_image().show()