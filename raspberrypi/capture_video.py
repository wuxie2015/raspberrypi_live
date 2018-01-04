# -*- coding: utf-8 -*-
from picamera import PiCamera
import time


class VideoCapture:
    def __init__(self):
        pass

    def init_camera(self):
        '''select and init camera
        0 for laptop inside camera
        1,2,3,.... for other cameras
        input: nothing
        output: videocapture object'''
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 26
        return camera

    def captuer_video(self, file_path):
        '''capture video
        input: none
        output: none'''
        camera = self.init_camera()
        camera.start_recording(file_path)
        time.sleep(120)
        camera.stop_recording()
        camera.close()

if __name__ == '__main__':
    vc_obj = VideoCapture()
    vc_obj.captuer_video('output.avi')
