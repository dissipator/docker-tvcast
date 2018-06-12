import pychromecast
import random

#device_name = "XBR-55X850D"
#cached_mc = {} 

#chromecasts = pychromecast.get_chromecasts()
#device = [cc.device.friendly_name for cc in chromecasts]
#cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_name)
#mc = cast.media_controller

def title_map():
    return {
        "really": "ホンマでっか!?ＴＶ",
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


def get_tv_title(tv_title):
    title_maps = dict(title_map())
    if tv_title in title_maps:
        return title_maps[tv_title]


def get_random_tv_title():
    title_maps = dict(title_map())
    title = random.choice(list(title_maps.values()))
    # store title to temp file
    # {}
    return title


def list_tv_status(video):
    tv_status_list = {}
    title_maps = dict(title_map())
    for key, value in title_maps.items():
        video_status = True
        try:
            video_url = video.parse_video_url(value)
            if not video_url: 
                raise Exception('Error video url not found')
        except:
            video_url = None
            video_status = False
        date  = video.get_date(value)
        tv_status_list[key] = {"title": value, "status": video_status, "date": date,  "video_url": video_url}
    return tv_status_list



#def get_media_controller(device_name):
#    if device_name not in cached_mc:
#        cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_name)
#        cached_mc[device_name] = cast.media_controller
#    return cached_mc[device_name]
#
#
#def play_video(video_url, device_name):
#    mc = get_media_controller(device_name)
#    mc.play_media(video_url, 'video/mp4')
#
#def stop_video(device_name):
#    mc = get_media_controller(device_name)
#    mc.stop()
#
#def pause_video(device_name):
#    mc = get_media_controller(device_name)
#    mc.pause()
#
#def stop_video(device_name):
#    mc = get_media_controller(device_name)
#    mc.stop()
