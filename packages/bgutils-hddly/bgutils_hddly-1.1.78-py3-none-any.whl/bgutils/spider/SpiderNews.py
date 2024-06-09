from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderNews(BaseSpider):
    newsTitle: str #新闻标题
    newsUrl: str #新闻地址url
    ctime: str  #新闻发布时间
    media_name: str #发布媒体
    keywords: str #关键词

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "news_data" #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
