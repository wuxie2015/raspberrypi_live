# -*- coding: utf-8 -*-
import threading
from capture_video import VideoCapture
import time
import os
from socket_client import SocketClient
from setting import HOST,PORT
import subprocess

con = threading.Condition()

class Sequence:
    def __init__(self,max_size):
        self.max_size = int(max_size)
        self.queue = []

    def put(self,data):
        if self.max_size > 0:
            if self.full():
                raise ValueError('Queue is full!')
            else:
                self._put(data)

    def get(self):
        if self._queue_size() > 0:
            result = self._get()
            empty_flag = False
        else:
            result = None
            empty_flag = True
        return result

    def empty(self):
        if self._queue_size() == 0:
            return True
        else:
            return False

    def full(self):
        if self._queue_size() == self.max_size:
            return True
        else:
            return False

    def _put(self,data):
        self.queue.append(data)

    def _get(self):
        result = self.queue[0]
        self.queue.pop(0)
        return result

    def _queue_size(self):
        return len(self.queue)

class ProduceVideo(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self, name=t_name)
        self.stopped = False
        self.video_capture = VideoCapture()
        self.queue = queue


    def gen_file_name(self):
        cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        file_name = "output_%s.avi" % cur_time
        file_path = os.path.join(os.getcwd(),file_name)
        return file_path

    def run(self):
        while not self.stopped:
            file_name = self.gen_file_name()
            self.video_capture.captuer_video(file_name)
            try:
                file_path = self.gen_file_name()
                self.video_capture.captuer_video(file_path)
                self.queue.put(file_path)
            except ValueError:
                while self.queue.full():
                    pass

    def stop(self):
        self.stopped = True

    def isstoped(self):
        return self.stopped


class PushStream(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self, name=t_name)
        self.stopped = False
        self.video_capture = VideoCapture()
        self.queue = queue
        self.socket_client = SocketClient(HOST,PORT)

    def run(self):
        while not self.stopped:
            if self.queue.empty():
                pass
            else:
                while not self.queue.empty():
                    file_path = self.queue.get()
                    subprocess.call("python /usr/local/project/raspberrypi_video/raspberrypi/socket_client.py -f %s"%file_path,
                    stdout=subprocess.PIPE,shell=True)
                    try:
                        os.system('rm -rf %s'%file_path)
                        print('rm -rf %s'%file_path)
                    except Exception as e:
                        print(e)
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(e)

    def stop(self):
        self.stopped = True

    def isstoped(self):
        return self.stopped

def test():
    sequence = Sequence(1000)
    thread1 = ProduceVideo('ProduceVideo',sequence)
    thread2 = PushStream('PushStream',sequence)
    thread1.start()
    thread2.start()

if __name__ == '__main__':
    test()
