#! /usr/bin/python
# -*- coding: utf-8 -*-
from python_push_rtmp import Writer
import python_push_rtmp
import librtmp
from picamera import PiCamera
import time
import os
from setting import HOST
import logging
from logging.handlers import RotatingFileHandler


class VideoCapture:
    def __init__(self):
        self.logger = self.logger_init()

    def logger_init(self):
        # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        log_file = 'capture_video.log'
        Rthandler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '\n%(asctime)s   %(filename)s[line:%(lineno)d]   %(levelname)s\n%(message)s')
        Rthandler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(Rthandler)
        logger.setLevel(logging.ERROR)
        return logger

    def init_camera(self):
        '''input: nothing
        output: videocapture object'''
        brightness = int(os.getenv('VIDEO_BRIGHTNESS', 70))
        width = int(os.getenv('VIDEO_WIDTH', 640))
        hight = int(os.getenv('VIDEO_HIGHT', 480))
        rotation = int(os.getenv('VIDEO_ROTATION', 180))
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
        return camera

    def gen_file_name(self):
        cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = "output_%s.h264" % cur_time
        file_path = os.path.join(os.getcwd(), file_name)
        return file_path

    def init_rtmp(self):
        conn = librtmp.RTMP(
            "rtmp://%s:1935/live/livestream" % HOST,  # 推流地址
            live=True)
        librtmp.librtmp.RTMP_EnableWrite(conn.rtmp)
        conn.connect()
        # 拼装视频格式的数据包
        meta_body_array = [python_push_rtmp.get_meta_string('@setDataFrame'), python_push_rtmp.get_meta_string('onMetaData'),
                           bytes(bytearray([0x08, 0x00, 0x00, 0x00, 0x06])),
                           # 两个字符串和ECMA array头，共计6个元素,注释掉了音频相关数据
                           python_push_rtmp.get_property_string(
                               'width'), python_push_rtmp.get_meta_double(640.0),
                           python_push_rtmp.get_property_string(
                               'height'), python_push_rtmp.get_meta_double(480.0),
                           python_push_rtmp.get_property_string(
                               'videodatarate'), python_push_rtmp.get_meta_double(0.0),
                           python_push_rtmp.get_property_string(
                               'framerate'), python_push_rtmp.get_meta_double(25.0),
                           python_push_rtmp.get_property_string(
                               'videocodecid'), python_push_rtmp.get_meta_double(7.0),
                           # get_property_string('audiodatarate'), get_meta_double(125.0),
                           # get_property_string('audiosamplerate'), get_meta_double(44100.0),
                           # get_property_string('audiosamplesize'), get_meta_double(16.0),
                           # get_property_string('stereo'), get_meta_boolean(True),
                           # get_property_string('audiocodecid'), get_meta_double(10.0),
                           python_push_rtmp.get_property_string(
                               'encoder'), python_push_rtmp.get_meta_string('Lavf57.56.101'),
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
                # camera.start_preview()
                Writer_obj = Writer(conn, meta_packet, start_time)
                # Writer_obj = librtmp.RTMPStream(conn)
                camera.start_recording(
                    Writer_obj,
                    format='h264',
                    intra_period=25,
                    quality=25)  # 开始录制，数据输出到Writer的对象里,quality从10到40,40最低
                camera.wait_recording(86400)
                camera.stop_recording()
                camera.close()
            except BaseException as e:
                self.logger.error(e)
                try:
                    camera.stop_recording()
                    camera.close()
                except BaseException as e:
                    break
                else:
                    continue


if __name__ == '__main__':
    vc_obj = VideoCapture()
    vc_obj.captuer_video()
