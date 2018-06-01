import service
from video import Video
from device import Device
import pdb

# docker test
# docker run -it --rm -v `pwd`:/app --privileged --net="host" --name flask local/tvcast bash

device_name = "XBR-55X850D"
device = Device(device_name)

def jp_tv_show(title):
    tv_title = service.get_tv_title(title)
    jp_video = Video.get_jp_video()
    video_url = jp_video.parse_video_url(tv_title)
    device.play_video(video_url)
    #device.stop_video()

    #service.play_video(video_url, device_name)

jp_tv_show('really')
