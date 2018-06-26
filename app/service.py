import pychromecast
import random
from multiprocessing import Pool 


def get_random_tv_title():
    title_maps = dict(title_map())
    title = random.choice(list(title_maps.values()))
    # store title to temp file
    # {}
    return title


def cast_tv(device, site_video, title, chapter = None):
        if title == 'random':
            tv_title = site_video.get_random_tv_title()
        else:
            tv_title = site_video.get_title(title.lower())
        try:
            video_url = site_video.parse_video_url(tv_title, chapter)
        except:
            return '{"status":"fail", "error":%s, "message":"error parsing url for %s"}' %(str(e), str(tv_title))
        device.play_video(video_url)
        return '{"status":"ok", "tv_title":tv_title}'


def list_tv_status(video):
    # https://stackoverflow.com/questions/3288595/multiprocessing-how-to-use-pool-map-on-a-function-defined-in-a-class
    # https://stackoverflow.com/questions/2846653/how-to-use-threading-in-python
    # sort list
    # sorted(student_tuples, key=lambda a: a[1])
    pool = Pool()
    title_maps = dict(title_map())
    label = [key for key in title_maps]
    titles = [value for key, value in title_maps.items()]
    video_urls = pool.map(video.parse_video_url ,titles)
    #tv_status_list = zip(titles, video_urls)
    tv_status_list = zip(*[label, titles, video_urls])
    #video_urls = pool.map(video.test ,["しゃべくり007"])
    #video_urls = pool.map(video.parse_video_url ,["adfasd"])
    pool.close()
    pool.join()
    return list(tv_status_list)

    #tv_status_list = {}
    #title_maps = dict(title_map())
    #for key, value in title_maps.items():
    #    video_status = True
    #    try:
    #        video_url = video.parse_video_url(value)
    #        if not video_url: 
    #            raise Exception('Error video url not found')
    #    except:
    #        video_url = None
    #        video_status = False
    #    date  = video.get_date(value)
    #    tv_status_list[key] = {"title": value, "status": video_status, "date": date,  "video_url": video_url}
    #return tv_status_list



