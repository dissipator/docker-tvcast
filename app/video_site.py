import json
import requests
import datetime
import re
from lxml import html

import urllib.request
from webdriver.default import DefaultWebDriver

class VideoSite(object):

    def __init__(self, site, xpaths, providers, domain=None, webdriver=None):
        self.site = site
        self.xpaths = xpaths 
        self.providers = providers 
        self.domain = domain
        self.title = None
        self.webdriver = DefaultWebDriver() if not webdriver else webdriver


    def parse_video_url(self, title=None, chapter=None):
        idx = 0
        xpaths_copy = list(self.xpaths)
        site_copy = self.site

        if title:
            site_copy = self.site.replace("@title@", title)
            self.replace_title(xpaths_copy, title)
        if chapter:
            site_copy = site_copy.replace("@chapter@", chapter)
            self.replace_chapter(xpaths_copy, chapter)
        if self.providers:
            self.replace_provider(xpaths_copy, self.providers[idx])

        """ parse each schema xpath """
        next_url = None
        for item in xpaths_copy:
            (key, xpath), = item.items()
            
            """ Get html content """
            if next_url:
                """ check if next_url contains domain """
                if self.domain and str(next_url).startswith('/') and self.domain not in str(next_url):
                    next_url = self.domain + next_url
                page = self.webdriver.get_html(next_url)
            else:
                page = self.webdriver.get_html(site_copy)

            """ xpath process types """
            if key == 'link':
                tree = html.fromstring(str.encode(page))
                links = tree.xpath(xpath)
                next_url = links[0] if links else None
            elif key == 'regex':
                match = re.search(xpath, str(page))
                next_url = match.group(1) if match else None
            elif key == 'date':
                continue

            if not next_url:
                return None

        # todo:
        # validate mp4 video link
        # if video link return 200 status
        # if validate fail call itself with idx = idx + 1
        return next_url


    def get_date(self, title):
        xpaths_copy = list(self.xpaths['video_date'])
        site_copy = self.site.replace("@title@", title)
        self.replace_title(xpaths_copy, title)

        next_url = None
        for xpath in xpaths_copy:
            if next_url:
                page = requests.get(next_url)
            else:
                page = requests.get(site_copy)
            tree = html.fromstring(page.content)
            links = tree.xpath(xpath)
            next_url = links[0]
        date = re.findall("[0-9]{1,2}月[0-9]{1,2}日", next_url)
        return date


    def replace_title(self, links, title):
        for idx, item in enumerate(links):
            """ get key & value from single dict """
            (key, path), = item.items()
            links[idx] = {key: path.replace("@title@", title)}


    def replace_provider(self, links, provider):
        for idx, item in enumerate(links):
            (key, path), = item.items()
            links[idx] = {key: path.replace("@provider@", provider)}


    def replace_chapter(self, links, chapter):
        for idx, item in enumerate(links):
            (key, path), = item.items()
            links[idx] = {key: path.replace("@chapter@", chapter)}


    @classmethod
    def get_waraimasu(self):
        site = 'http://waraimasu.blog40.fc2.com/?q=@title@'
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
        providers = ["9TSU", "PAN"]
        return self(site, xpaths, providers) 


    @classmethod
    def get_99kubo(self):
        # http://www.99tw.net/redirect?mode=xplay&id={vid}&pid={chapter}
        site = 'http://www.99tw.net/redirect?mode=xplay&id=@title@&pid=@chapter@'
        # "480P.*src\\:\\s?\\'(.*)\\'"
        xpaths = [
            {"regex": r'480P.*src\:\s?\'(.*)\''}
        ]
        providers = None
        domain = 'http://www.99kubo.tv'
        return self(site, xpaths, providers, domain) 


