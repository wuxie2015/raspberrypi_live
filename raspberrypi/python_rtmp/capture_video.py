#! /usr/bin/python
# -*- coding: utf-8 -*-
import librtmp
import time
import os
import traceback
from picamera import PiCamera
from raspberrypi.python_rtmp.python_push_rtmp import Writer,get_meta_string,get_property_string,get_meta_double
from raspberrypi.python_rtmp.setting import HOST,PORT
from raspberrypi.python_rtmp.logger import Logger


class VideoCapture:
    def __init__(self):
        self.logger = Logger.get_logger()

    def init_camera(self):
        '''input: nothing
        output: videocapture object'''
        brightness = int(os.getenv('VIDEO_BRIGHTNESS', 70))
        width = int(os.getenv('VIDEO_WIDTH', 640))
        hight = int(os.getenv('VIDEO_HIGHT', 480))
        rotation = int(os.getenv('VIDEO_ROTATION', 90))
        framerate = int(os.getenv('VIDEO_FRAMERATE', 25))
        self.logger.info('brightness %s' % brightness)
        self.logger.info('width %s' % width)
        self.logger.info('hight %s' % hight)
        self.logger.info('rotation %s' % rotation)
        self.logger.info('framerate %s' % framerate)
        camera = PiCamera()
        camera.resolution = (width, hight)
        camera.rotation = int(rotation)
        camera.framerate = framerate
        camera.brightness = brightness
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'
        return camera

    def gen_file_name(self):
        cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = "output_%s.h264" % cur_time
        file_path = os.path.join(os.getcwd(), file_name)
        return file_path

    def init_rtmp(self):
        conn = librtmp.RTMP(
            "rtmp://%s:%s/live/livestream" % (HOST,PORT),  # 推流地址
            live=True)
        librtmp.librtmp.RTMP_EnableWrite(conn.rtmp)
        conn.connect()
        # 拼装视频格式的数据包
        meta_body_array = [get_meta_string('@setDataFrame'), get_meta_string('onMetaData'),
                           bytes(bytearray([0x08, 0x00, 0x00, 0x00, 0x06])),
                           # 两个字符串和ECMA array头，共计6个元素,注释掉了音频相关数据
                           get_property_string(
                               'width'), get_meta_double(640.0),
                           get_property_string(
                               'height'), get_meta_double(480.0),
                           get_property_string(
                               'videodatarate'), get_meta_double(0.0),
                           get_property_string(
                               'framerate'), get_meta_double(25.0),
                           get_property_string(
                               'videocodecid'), get_meta_double(7.0),
                           # get_property_string('audiodatarate'), get_meta_double(125.0),
                           # get_property_string('audiosamplerate'), get_meta_double(44100.0),
                           # get_property_string('audiosamplesize'), get_meta_double(16.0),
                           # get_property_string('stereo'), get_meta_boolean(True),
                           # get_property_string('audiocodecid'), get_meta_double(10.0),
                           get_property_string(
                               'encoder'), get_meta_string('Lavf57.56.101'),
                           bytes(bytearray([0x00, 0x00, 0x09]))
                           ]
        meta_body = ''.join(meta_body_array)
        meta_packet = librtmp.RTMPPacket(
            type=librtmp.PACKET_TYPE_INFO,
            format=librtmp.PACKET_SIZE_LARGE,
            channel=0x04,
            timestamp=0,
            body=meta_body)
        meta_packet.packet.m_nInfoField2 = 1  # 修改stream id
        stream = conn.create_stream(writeable=True)
        return (conn, meta_packet, stream)

    def captuer_video(self):
        '''capture video
        input: none
        output: none'''

        while True:
            try:
                camera = self.init_camera()
                start_time = time.time()
                (conn, meta_packet, stream_rtmp) = self.init_rtmp()
                Writer_obj = Writer(conn, meta_packet, start_time)
                camera.start_recording(
                    Writer_obj,
                    format='h264',
                    intra_period=25,
                    quality=25)  # 开始录制，数据输出到Writer的对象里,quality从10到40,40最低
                camera.wait_recording(43200)
                camera.stop_recording()
                camera.close()
            except BaseException as e:
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
                try:
                    camera.stop_recording()
                    camera.close()
                except BaseException as e:
                    self.logger.critical(e)
                else:
                    continue

if __name__ == '__main__':
    vc_obj = VideoCapture()
    vc_obj.captuer_video()
