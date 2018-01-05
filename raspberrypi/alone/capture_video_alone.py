# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from picamera import PiCamera
import time
import os
from rabbitmq_util import producer
import pika

class VideoCapture:
    def __init__(self):
        pass

    def init_camera(self):
        '''input: nothing
        output: videocapture object'''
        brightness = os.getenv('video_brightness',70)
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 25
        camera.brightness = brightness
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
        mq_obj = producer.mq_producer()
        camera = self.init_camera()
        file_path = self.gen_file_name()
        camera.start_recording(file_path)
        time.sleep(120)
        camera.stop_recording()
        camera.close()
        mq_obj.put_message(file_path)
        mq_obj.close()

if __name__ == '__main__':
    vc_obj = VideoCapture()
    while True:
        try:
            vc_obj.captuer_video()
        except Exception:
            continue
