import json
import requests
from lxml import html

class Video(object):
    def __init__(self, site, xpaths, providers):
        self.site = site
        self.xpaths = xpaths 
        self.providers = providers 
        self.title = None
        self.session = 1


    def parse_video_url(self, title):
        idx = 0
        xpaths_copy = list(self.xpaths)
        self.replace_title(xpaths_copy, title)
        self.replace_provider(xpaths_copy, self.providers[idx])

        next_url = None
        for xpath in xpaths_copy:
            if next_url:
                page = requests.get(next_url)
            else:
                page = requests.get(self.site)
            tree = html.fromstring(page.content)
            links = tree.xpath(xpath)
            next_url = links[0]
        # todo:
        # validate mp4 video link
        # if video link return 200 status
        # if validate fail call itself with idx = idx + 1
        return next_url


    def replace_title(self, links, title):
        for idx, item in enumerate(links):
            links[idx] = item.replace("@title@", title)


    def replace_provider(self, links, provider):
        for idx, item in enumerate(links):
            links[idx] = item.replace("@provider@", provider)


    @classmethod
    def get_jp_video(self):
        site = 'http://waraimasu.blog40.fc2.com/'
        # xpath schema
        xpaths = [ 
            # 1 homepage
            '//a[text()="@title@"]/@href',
            # 2 TV show page
            "//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/@href",
            # 3 video provider
            '//a[text()="@provider@"]/@href',
            #'//a[contains(text(),"@provider@")]/@href',
            # 4 video mp4
            "//div[contains(@id, 'video-content')]//video/@src"
        ]
        providers = ["9TSU"]
        return self(site, xpaths, providers) 
