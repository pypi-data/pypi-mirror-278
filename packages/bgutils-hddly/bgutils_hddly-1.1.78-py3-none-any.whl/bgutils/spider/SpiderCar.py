from dataclasses import dataclass
from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderCar(BaseSpider):
    title: str #小车名称
    style: str #小车类型
    desc: str #书描述
    price: str #车价
    pic: str #车图片
    regdate: str #注册日期
    distance: str #行驶路程


    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username  #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "books_data"  #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
