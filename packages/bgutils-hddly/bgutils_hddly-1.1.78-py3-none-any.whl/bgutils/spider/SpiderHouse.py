from dataclasses import dataclass
from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider
@dataclass
class SpiderHouse(BaseSpider):
    title: str #房产标题
    addr: str  #地址
    houseinfo: str #房屋信息
    houseurl: str #房屋url
    price : str #房总价
    unitprice : str #房单价
    img : str #图片
    city : str  # 所在城市

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "house_data" #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充




