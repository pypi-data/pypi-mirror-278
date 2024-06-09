from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderCourse(BaseSpider):
    title: str #课程标题
    author: str #书作者
    link: str #课程链接
    desc: str #课程描述
    tags: str #标签
    price: str #课程单价
    pic: str #课程图片

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username  #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "course_data"  #课程题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充