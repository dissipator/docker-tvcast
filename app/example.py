import time
import pychromecast
import requests
from lxml import html
# find . -type f -name '*.py' -not -path "./vendored/*" | xargs python2 -m py_compile
def play(video_url):
    chromecasts = pychromecast.get_chromecasts()
    device = [cc.device.friendly_name for cc in chromecasts]
    print(device)

    cast = next(cc for cc in chromecasts if cc.device.friendly_name == "XBR-55X850D")
    cast.wait()
    print(cast.device)

    #video_url = 'http://174.35.21.65/redirect/trans-idx.gcdn.pandora.tv/flvorgx.pandora.tv/hd/_user/r/a/rakuroom/31/201805092159024504vwk3uddwv95x.flv?key1=41423341433032323632323131353331353630353931384538443841&key2=A87BF35CF6990E4DAEC35A1EF408D9&ft=FC&class=normal&country=CA&pcode2=60103&px-bps=15253504&px-bufahead=3&cms=1&rand=27&px-time=1526372182&px-hash=f54ade204ad8ceac341f6b7f84522cbb'

    mc = cast.media_controller
    mc.play_media(video_url, 'video/mp4')
    mc.block_until_active()
    mc.play()

    #[cc.device.friendly_name for cc in chromecasts]

def get_link():
    website = 'http://waraimasu.blog40.fc2.com/'
    tv_title = "ホンマでっか!?ＴＶ" 
    video_provider = "9TSU"

    # 1 homepage
    page = requests.get(website)
    tree = html.fromstring(page.content)
    #links = tree.xpath('//a[text()="ホンマでっか!?ＴＶ"]/@href')
    links = tree.xpath('//a[text()="%s"]/@href' % tv_title)
    link = links[0]
    print(link)

    # 2 TV show page
    page = requests.get(link)
    tree = html.fromstring(page.content)
    links = tree.xpath("//div[contains(@class,'ently_outline')]//div[contains(@class, 'readmore')]//a[contains(@onclick,'showMore')]/@href")
    link = links[0]
    print(link)

    # 3 video provider
    page = requests.get(link)
    tree = html.fromstring(page.content)
    links = tree.xpath('//a[text()="%s"]/@href' % video_provider)
    link = links[0]
    print(link)

    # third page
    page = requests.get(link)
    tree = html.fromstring(page.content)
    links = tree.xpath("//div[contains(@id, 'video-content')]//video/@src")
    link = links[0]
    print(link)
    return link



url = get_link()
play(url)
