from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
from mtl.settings import UAPOOL

class Uamid(UserAgentMiddleware):
    def __init__(self,ua=''):
        self.user_agent=ua
    def process_request(self, request, spider):
        thisua=random.choice(UAPOOL)
        print("当前的用户代理是:"+str(thisua))
        request.headers.setdefault("User-Agent",thisua)