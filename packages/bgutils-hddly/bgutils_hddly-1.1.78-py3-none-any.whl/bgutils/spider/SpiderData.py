from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderData(BaseSpider):
    id: str
    title: str
    url: str
    price: str
    pic: str
    time_sort: str

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username
        self.collector= collector
        self.topic = "goods_data"
        self.rawurl= rawurl
        self.rawdata = rawdata
        self.coll_time = datetime.now()
