import json
import datetime
from video_site.video_site import VideoSite
from webdriver.default import DefaultWebDriver


class Kubo(VideoSite):

    def __init__(self):
        site = 'http://www.99tw.net/redirect?mode=xplay&id=@title@&pid=@chapter@'
        xpaths = self.get_xpaths()
        providers = None
        domain = 'http://www.99kubo.tv'
        webdriver = DefaultWebDriver()
        super().__init__(site, xpaths, providers, domain, webdriver)


    @classmethod
    def title_map(cls):
        return {
            "one piece": "26351",
            "bleach": "32800",
            "titan": "91998"
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
            {"regex": r'480P.*src\:\s?\'(.*)\''}
            #[{"regex": r'480P.*src\:\s?\'(.*)\''}, {"regex": r'360P.*src\:\s?\'(.*)\''}]
        ]
        return xpaths


    def get_random_tv_title(self):
        title_maps = dict(self.title_map())
        title = random.choice(list(title_maps.values()))
        return title


    def list_tv_status(self):
        # not support
        pass
