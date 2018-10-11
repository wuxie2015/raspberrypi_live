#! /usr/bin/python
# -*- coding: utf-8 -*-
import time

def feed_dog():
    with open("watchdog_record.txt","w") as f:
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(cur_time)