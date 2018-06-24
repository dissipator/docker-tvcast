import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class ChromeWebDriver(object):

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = '/usr/bin/google-chrome'
        self.driver_path = '/usr/bin/chromedriver'
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=chrome_options)


    def get_html(self, url):
        """ web driver interface """
        self.driver.get(url)
        return self.driver.page_source
