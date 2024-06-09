import abc
import json
from dataclasses import dataclass

@dataclass
class BaseSpider(metaclass=abc.ABCMeta):

    topic: str #采集题材，如music_data,jobs_data
    rawurl: str #采集的原始url地址
    rawdata: str #采集的原始数据，如记录行的json内容
    username: str #采集者学号
    collector: str #采集者姓名
    coll_time: str #采集时间，实体初始方法自动填充

    def __init__(self, username, collector, topic, rawurl, rawdata):
        return

