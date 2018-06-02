import pychromecast

class Device(object):

    #cached_mc = None 

    def __init__(self, device_name = "XBR-55X850D"):
        self.cached_mc = None 
        self.device_name = device_name
        #self.chromecasts = pychromecast.get_chromecasts()
        #self.device_list = [cc.device.friendly_name for cc in self.chromecasts]


    def get_media_controller(self):
        if not self.cached_mc:
            self.chromecasts = pychromecast.get_chromecasts()
            cast = next(cc for cc in self.chromecasts if cc.device.friendly_name == self.device_name)
            self.cached_mc = cast.media_controller
        return self.cached_mc


    def play_video(self, video_url):
        mc = self.get_media_controller()
        mc.play_media(video_url, 'video/mp4')


    def stop_video(self):
        mc = self.get_media_controller()
        mc.stop()
        

    def pause_video(self):
        mc = self.get_media_controller()
        mc.pause()

    def resume_video(self):
        mc = self.get_media_controller()
        mc.play()


    def seek_video(self, mins):
        seconds = (int(mins) * int(60))
        mc = self.get_media_controller()
        mc.seek(seconds)


    def skip_video(self):
        mc = self.get_media_controller()
        mc.skip()
