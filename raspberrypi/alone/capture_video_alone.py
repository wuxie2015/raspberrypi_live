#! /usr/bin/python
# -*- coding: utf-8 -*-
from picamera import PiCamera
import time
import os
from rabbitmq_util import producer
import logging
from logging.handlers import RotatingFileHandler
from io import BytesIO

class VideoCapture:
    def __init__(self):
        self.logger = self.logger_init()

    def logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'capture_video_alone.log'
        Rthandler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.DEBUG)
        return logger

    def init_camera(self):
        '''input: nothing
        output: videocapture object'''
        brightness = int(os.getenv('VIDEO_BRIGHTNESS',70))
        width = int(os.getenv('VIDEO_WIDTH', 640))
        hight = int(os.getenv('VIDEO_HIGHT',480))
        rotation = int(os.getenv('VIDEO_ROTATION',180))
        framerate = int(os.getenv('VIDEO_FRAMERATE',25))
        print('brightness',brightness)
        print('width',width)
        print('hight',hight)
        print('rotation',rotation)
        print('framerate',framerate)
        camera = PiCamera()
        camera.resolution = (width, hight)
        camera.rotation = int(rotation)
        camera.framerate = framerate
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
        while True:
            try:
                interval = int(os.getenv('VIDEO_INTERVAL', 2))
                mq_obj = producer.mq_producer()
                camera = self.init_camera()
                file_path = self.gen_file_name()
                camera.start_recording(file_path)
                time.sleep(interval)
                camera.stop_recording()
                camera.close()
                mq_obj.put_message(file_path)
                mq_obj.close()
            except Exception as e:
                self.logger.error(e)
                continue

if __name__ == '__main__':
    vc_obj = VideoCapture()
    vc_obj.captuer_video()

