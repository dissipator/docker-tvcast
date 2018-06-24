import os
import json
import requests

class DefaultWebDriver(object):

    def __init__(self):
        pass


    def get_html(self, url):
        """ web driver interface """
        page = requests.get(url)
        return page.content.decode("utf-8")
