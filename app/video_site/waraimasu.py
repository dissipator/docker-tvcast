import json
import datetime
import random
from video_site.video_site import VideoSite
from webdriver.default import DefaultWebDriver
from multiprocessing import Pool 


class Waraimasu(VideoSite):

    def __init__(self):
        site = 'http://waraimasu.blog40.fc2.com/?q=@title@'
        xpaths = self.get_xpaths()
        providers = ["9TSU", "PAN"]
        domain = None
        webdriver = DefaultWebDriver()
        super().__init__(site, xpaths, providers, domain, webdriver)


    @classmethod
    def title_map(cls):
        return {
            "really": "ホンマでっか!?TV",
            "going": "イッテＱ",
            "7": "しゃべくり007",
            "sport": "炎の体育会TV",
            "class": "世界一受けたい授業",
            "look": "世界まる見えテレビ特捜部",
            "lawyer": "行列のできる法律相談所",
            "talk": "深イイ話",
            "karaoke": "THEカラオケ★バトル",
            "music": "ミュージックステーション",
            "bingo": "AKBINGO",
            "gold": "金スマ",
            "london": "ロンドンハーツ",
            "monitoring": "モニタリング",
            "news": "ザ!世界仰天ニュース",
            "seminar": "有吉ゼミ",
            "girl": "幸せ!ボンビーガール",
            "tonight": "今夜くらべてみました"
        }


    @classmethod
    def get_title(cls, title):
        title_maps = dict(cls.title_map())
        if title in title_maps:
            return title_maps[title]


    @classmethod
    def get_xpaths(cls):
        # xpath schema
        xpaths = [
            {"date": "//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/text()"},
            # 2 TV show page
            {"link": "//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/@href"},
            # 3 video provider
            {"link":'//a[contains(text(),"@provider@")]/@href'},
            # 4 video mp4
            {"link":"//div[contains(@id, 'video-content')]//video/@src"}
        ]
        return xpaths


    def get_random_tv_title(self):
        title_maps = dict(self.title_map())
        title = random.choice(list(title_maps.values()))
        return title


    def list_tv_status(self):
        pool = Pool()
        title_maps = dict(self.title_map())
        label = [key for key in title_maps]
        titles = [value for key, value in title_maps.items()]
        video_urls = pool.map(self.parse_video_url ,titles)

        tv_status_list = []
        for idx, title in enumerate(titles):
            tv_status_list.append({"title": title, "label": label[idx], "url": video_urls[idx]})
        #tv_status_list = zip(*[label, titles, video_urls])

        # write to tmp file, and time stamp, only refresh if time - now > 6 hrs

        
        pool.close()
        pool.join()
        #return list(tv_status_list)
        return tv_status_list
