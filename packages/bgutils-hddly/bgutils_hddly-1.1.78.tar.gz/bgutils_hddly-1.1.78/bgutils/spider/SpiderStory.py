from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderStory(BaseSpider):
    title: str #故事标题
    author: str #故事作者
    link: str #故事详情链接
    desc: str #故事描述
    content: str #故事内容
    pic: str #故事图片

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username  #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "storys_data"  #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
