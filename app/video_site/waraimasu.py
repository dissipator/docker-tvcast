import json
import datetime
import time
import random
from video_site.video_site import VideoSite
from webdriver.default import DefaultWebDriver
from multiprocessing import Pool 


class Waraimasu(VideoSite):

    def __init__(self):
        #site = 'http://waraimasu.blog40.fc2.com/?q=@title@'
        site = 'http://waraimasu.blog40.fc2.com/blog-category-@title@.html'
        xpaths = self.get_xpaths()
        providers = ["9TSU", "PAN"]
        domain = 'http://waraimasu.blog40.fc2.com'
        webdriver = DefaultWebDriver()
        super().__init__(site, xpaths, providers, domain, webdriver)


    @classmethod
    def title_map(cls):
        #return {
        #    "really": "ホンマでっか!?TV",
        #    "going": "イッテＱ",
        #    "7": "しゃべくり007",
        #    "sport": "炎の体育会TV",
        #    "class": "世界一受けたい授業",
        #    "look": "世界まる見えテレビ特捜部",
        #    "lawyer": "行列のできる法律相談所",
        #    "talk": "深イイ話",
        #    "karaoke": "THEカラオケ★バトル",
        #    "music": "ミュージックステーション",
        #    "bingo": "AKBINGO",
        #    "gold": "金スマ",
        #    "london": "ロンドンハーツ",
        #    "monitoring": "モニタリング",
        #    "news": "ザ!世界仰天ニュース",
        #    "seminar": "有吉ゼミ",
        #    "girl": "幸せ!ボンビーガール",
        #    "tonight": "今夜くらべてみました",
        #    # New #
        #    "regret": "有吉反省会",
        #    "deep": "深イイ話",
        #    "news": "池上彰のニュースそうだったのか",
        #    "quize": "Qさま",
        #    "laugh": "笑ってコラえて",
        #    "world": "世界仰天ニュース",
        #    "neputune": "ネプリーグ",
        #    "surprise": "世界が驚いたニッポンスゴ〜イデスネ",
        #    "ear": "林先生の初耳学",
        #    "unbelivable": "奇跡体験アンビリバボー",
        #    "do": "嵐にしやがれ",
        #    "versus": "VS嵐",
        #    "song": "utage",
        #    "medical": "みんなの家庭の医学",
        #}
        return {
            "really": "82",
            "going": "22",
            "7": "74",
            "sport": "169",
            "class": "329",
            "look": "344",
            "lawyer": "194",
            "talk": "241",
            "karaoke": "557",
            "music": "418",
            "bingo": "293",
            "gold": "303",
            "london": "37",
            "monitoring": "232",
            "news": "331",
            "seminar": "353",
            "girl": "286",
            "tonight": "228",
            "regret": "274",
            "deep": "241",
            "news": "687",
            "quize": "234",
            "laugh": "345",
            "world": "331",
            "neputune": "151",
            "surprise": "607",
            "ear": "693",
            "unbelivable": "266",
            "do": "318",
            "versus": "317",
            "song": "521",
            "medical": "453"
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
            #{"date": "//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/text()"},
            # 2 TV show page
            #{"link": "//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/@href"},
            #{"link": "//div[contains(@id,'searchmain')]//ul//li//a/@href"},
            {"link": "//div[contains(@class,'readmore')]//p//a/@href"},
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


    def get_key(self):
        return 'waraimasu_status'


    def list_tv_status(self):
        store_key = self.get_key()
        status_cache = None
        # cache for 6 hours
        cache_expire = 21600 
        try:
            status_cache = self.fetch_info(store_key)
            if (int(time.time()) - status_cache['time']) > cache_expire :
                status_cache = None
        except FileNotFoundError as e:
            pass

        if status_cache:
            return status_cache["body"]

        pool = Pool()
        title_maps = dict(self.title_map())
        label = [key for key in title_maps]
        titles = [value for key, value in title_maps.items()]
        video_urls = pool.map(self.parse_video_url ,titles)

        tv_status_list = []
        for idx, title in enumerate(titles):
            tv_status_list.append({"title": title, "label": label[idx], "status": "True" if video_urls[idx] else "False", "url": video_urls[idx]})
        #tv_status_list = zip(*[label, titles, video_urls])

        pool.close()
        pool.join()
        # write to tmp file, and time stamp, only refresh if time - now > 6 hrs
        self.save_info(store_key, {"time": int(time.time()), "body": tv_status_list})
        return tv_status_list


    def clear_status_cache(self):
        store_key = self.get_key()
        self.delete_info(store_key)
