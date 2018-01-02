# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
try:
    from server.rabbitmq_util import consumer
except ModuleNotFoundError:
    from rabbitmq_util import consumer

def scan_file(path):
    f_name_list = os.listdir(path)
    if len(f_name_list)> 0:
        for f_name in f_name_list:
            f_name_split = f_name.split('.')
            extension = f_name_split[-1]
            if extension == 'avi':
                file_path = os.path.join(path,f_name)
                os.system(
                     "ffmpeg -re -i %s -vcodec libx264 -acodec copy -f flv -y rtmp://118.126.65.199:1935/live/livestream;" % file_path)
                shutil.move(file_path,str(file_path)+'.bak')
                # os.remove(file_path)

def scan_queue_file(ch, method, properties, body):
    f_name = body
    file_path = str(f_name.decode('utf8'))
    print(file_path)
    subprocess.call("ffmpeg -re -i %s -vcodec libx264 -acodec copy -f flv -y rtmp://118.126.65.199:1935/live/livestream;" % file_path,
                    stdout=subprocess.PIPE,shell=True)
    # os.system(
    #     "ffmpeg -re -i %s -vcodec libx264 -acodec copy -f flv -y rtmp://118.126.65.199:1935/live/livestream;" % file_path)
    shutil.move(file_path, str(file_path) + '.bak')


if __name__ == '__main__':
    # while True:
    #     scan_file('/usr/local/project/tmp_video/')
    mq_obj = consumer.mq_consumer()
    mq_obj.init_consumer(scan_queue_file)