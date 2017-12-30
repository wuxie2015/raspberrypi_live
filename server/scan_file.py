# -*- coding: utf-8 -*-
import os
import shutil

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

if __name__ == '__main__':
    while True:
        scan_file('/usr/local/project/tmp_video/')