from flask import Flask
import service
from video import Video
from device import Device
import json


app = Flask(__name__)
application = app

device_name = "XBR-55X850D"
device = Device(device_name)
jp_video = Video.get_waraimasu()


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World in the docker!"


@app.route('/apple')
def apple():
    return "This is docker apple!"


# /jp/tv_show/really
@app.route('/tv/jp/<title>')
def tv_jp_show(title):
    if title == 'random':
        tv_title = service.get_random_tv_title()
    else:
        tv_title = service.get_tv_title(title.lower())
    try:
        video_url = jp_video.parse_video_url(tv_title)
    except:
        return '{"status":"fail", "error":%s, "message":"error parsing url for %s"}' %(str(e), str(tv_title))
    device.play_video(video_url)
    return '{"status":"ok", "tv_title":tv_title}'


@app.route('/tv/stop')
def stop_tv():
    device.stop_video()
    return '{"status":"ok", "msg":"video stoped"}'


@app.route('/tv/pause')
def pause_tv():
    device.pause_video()
    return '{"status":"ok", "msg":"video paused"}'


@app.route('/tv/resume')
def resume_tv():
    device.resume_video()
    return '{"status":"ok", "msg":"video resumed"}'


@app.route('/tv/seek/<mins>')
def seek_tv(mins):
    device.seek_video(mins)
    return '{"status":"ok", "msg":"video resumed"}'


@app.route('/tv/list')
def list_tv():
    title_list = service.title_map()
    return json.dumps(title_list)


@app.route('/tv/list/status')
def list_tv_status():
    tv_status = service.list_tv_status(jp_video)
    return json.dumps(tv_status)


# use by direct execute 
if __name__=='__main__':
        #app.run(host= '192.168.3.103', port=5000)
        app.run()
