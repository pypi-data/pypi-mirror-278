from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderGoods(BaseSpider):
    id: str #商品ID
    title: str #商品标题
    url: str #商品url
    price: str #商品的单价
    pic: str #商品的图片url
    time_sort: str #商品的顺序号

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "goods_data" #采集题材
        self.rawurl= rawurl  #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
