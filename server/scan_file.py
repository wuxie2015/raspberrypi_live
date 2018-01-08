# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
try:
    from server.rabbitmq_util import consumer
except ModuleNotFoundError:
    from rabbitmq_util import consumer


def scan_queue_file(ch, method, properties, body):
    f_name = body
    file_path = str(f_name.decode('utf8'))
    print(file_path)
    subprocess.call("ffmpeg -re -i %s -vcodec libx264 -acodec copy -f flv -y rtmp://127.0.0.1:1935/live/livestream;" % file_path,
                    stdout=subprocess.PIPE,shell=True)
    shutil.move(file_path, str(file_path) + '.bak')


if __name__ == '__main__':
    mq_obj = consumer.mq_consumer()
    mq_obj.init_consumer(scan_queue_file)
