from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderMeishi(BaseSpider):
    uid: str #商品ID
    username: str #作者
    title: str #商品标题
    mainingredient: str #原材料
    dateline :str #日期
    subject:str #主题
    url: str #商品url
    pic: str #商品的图片url,对应fcover

    # {
    #   "uid": "7796837",
    #   "username": "宸·羽",
    #   "id": "659229",
    #   "title": "香煎肉饼",
    #   "message": "",
    #   "mainingredient": "猪肉、木薯粉、虾皮、香菜、小葱、油、盐、蚝油、胡椒粉、五香粉、清水。",
    #   "dateline": "2024-5-28",
    #   "subject": "香煎肉饼",
    #   "fcover": "https://i3.meishichina.com/attachment/recipe/2024/05/29/2024052917169480832751.jpg?x-oss-process=style/c640",
    #   "cover": "https://i8.meishichina.com/attachment/recipe/2024/05/28/2024052817169106179691987796837.jpg?x-oss-process=style/f320x240",
    #   "mpic": "https://i3.meishichina.com/attachment/recipe/2024/05/29/2024052917169480832751.jpg?x-oss-process=style/c320",
    #   "tvpic": "attachment/recipe/2024/05/28/2024052817169106179691987796837.jpg",
    #   "mscover": "https://i3.meishichina.com/attachment/recipe/2024/05/29/2024052917169480832751.jpg?x-oss-process=style/c320",
    #   "path": "attachment/recipe/2024/05/28",
    #   "picname": "2024052817169106179691987796837.jpg",
    #   "collnum": "132",
    #   "viewnum": 0,
    #   "replynum": 0,
    #   "copyright": "1",
    #   "c320": "https://i3.meishichina.com/attachment/recipe/2024/05/29/2024052917169480832751.jpg?x-oss-process=style/c320",
    #   "avatar": "https://i5.meishichina.com/data/avatar/007/79/68/37_avatar_big.jpg?x-oss-process=style/c80",
    #   "likenum": 0,
    #   "isfav": 0,
    #   "islike": 0,
    #   "wapurl": "https://m.meishichina.com/recipe/all/elite/"
    # }

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "meishi_data" #采集题材
        self.rawurl= rawurl  #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
