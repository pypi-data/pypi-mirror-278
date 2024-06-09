from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderMusic(BaseSpider):
    id: str  #ID,如"222666"
    song_url: str #歌曲url
    song_name: str  #歌曲名
    artist_url: str #歌手url
    artist_name: str #歌手名
    album_name: str #专辑名
    album_url: str #专辑url

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "music_data" #采集题材
        self.rawurl= rawurl #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
