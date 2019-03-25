这是用来爬取www.meitulu.com图片的爬虫，基于scrapy框架搭建，使用python3.X语言。

详细教程：
https://www.52pojie.cn/thread-854416-1-1.html
https://www.52pojie.cn/thread-854893-1-1.html

为保护个人密码不被泄露，特更新程序密码保存方式，不上传github但自己可以使用。
请下载程序后，在此文件的下级目录./mtl/
增加新文件passwd.py
内部内容如下：
class passwd(object):
    def __init__(self):
        self.user="数据库用户名"
        self.password="数据库密码"
        self.host="数据库ip地址"
    def getUser(self):
        return self.user
    def getpasswd(self):
        return self.password
    def getHost(self):
        return self.host


如此，即可正常使用。