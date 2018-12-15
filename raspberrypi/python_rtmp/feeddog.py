#! /usr/bin/python
# -*- coding: utf-8 -*-
import time
import os

def feed_dog():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "watchdog_record.txt"
    file_path = os.path.join(file_dir,file_name)
    with open(file_path,"w") as f:
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(cur_time)