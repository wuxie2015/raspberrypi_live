#! /usr/bin/python
# -*- coding:utf-8 -*-

import cv2
import os
import glob

def split_img(window_size=64):
    images = glob.glob('test\\picture\\*.png')
    for img_item in images:
        file_name = img_item.split('\\')[2].split('.')[0]
        img = cv2.imread(img_item, cv2.IMREAD_GRAYSCALE)
        x_steps = img.shape[0]//window_size
        y_steps = img.shape[1]//window_size
        for x in range(x_steps):
            for y in range(y_steps):
                img_splited = img[x*window_size:(x+1)*window_size,y*window_size:(y+1)*window_size]
                # cv2.imshow("合成", img_splited)
                image_name = "non-vehicles\\" + file_name + "_" + str(x) + "_" + str(y) + ".png"
                cv2.imwrite(image_name, img_splited)


if __name__ == '__main__':
    split_img()