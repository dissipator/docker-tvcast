from flask import Flask
from flask import render_template
from device import Device
import service
import json
from video_site.kubo import Kubo
from video_site.waraimasu import Waraimasu

app = Flask(__name__)
application = app

device_name = "XBR-55X850D"
device = Device(device_name)
tv_site = Waraimasu()
animate_site = Kubo()


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World in the docker!"


""" JP TV """
# /jp/tv_show/really
@app.route('/tv/jp/<title>')
def tv_jp_show(title):
    return service.cast_tv(device, tv_site, title)


@app.route('/tv/list')
def list_tv():
    title_list = tv_site.title_map()
    return json.dumps(title_list)


@app.route('/tv/list/status')
def list_tv_status():
    tv_status = tv_site.list_tv_status()
    return render_template('tv_status.html', tv_status=tv_status)
    #return json.dumps(tv_status)


@app.route('/tv/list/status/clear')
def list_tv_status():
    tv_status = tv_site.clear_status_cache()
    return '{"status":"ok", "message":"status cache is deleted"}'


""" Animation """
@app.route('/tv/one-piece/<chapter>')
def tv_one_piece(chapter):
    return service.cast_tv(device, animate_site, 'one piece', chapter)


@app.route('/tv/bleach/<chapter>')
def tv_bleach(chapter):
    return service.cast_tv(device, animate_site, 'bleach', chapter)


@app.route('/tv/titan/<chapter>')
def tv_titan(chapter):
    return service.cast_tv(device, animate_site, 'titan', chapter)


""" Cast Controls """
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


# use by direct execute 
if __name__=='__main__':
        #app.run(host= '192.168.3.103', port=5000)
        app.run()
