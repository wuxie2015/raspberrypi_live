# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from picamera import PiCamera
import time
import os
from rabbitmq_util import producer

class VideoCapture:
    def __init__(self):
        self.mq_obj = producer.mq_producer()

    def init_camera(self):
        '''input: nothing
        output: videocapture object'''
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 26
        return camera

    def gen_file_name(self):
        cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = "output_%s.h264" % cur_time
        file_path = os.path.join(os.getcwd(),file_name)
        return file_path

    def captuer_video(self):
        '''capture video
        input: none
        output: none'''
        camera = self.init_camera()
        file_path = self.gen_file_name()
        camera.start_recording(file_path)
        time.sleep(120)
        camera.stop_recording()
        camera.close()
        self.mq_obj.put_message(file_path)

if __name__ == '__main__':
    vc_obj = VideoCapture()
    while True:
        vc_obj.captuer_video()
