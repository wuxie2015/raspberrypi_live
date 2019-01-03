# -*- coding:utf-8 -*-
#! /usr/bin/python
import cv2
import numpy as np
from raspberrypi.machinelearning.hog_features import Hog_descriptor
import math
import matplotlib.pyplot as plt


# 参考https://zhuanlan.zhihu.com/p/35607432

class HogPyramid:
    def __init__(self,img,cell_size=8,window_size=64,cells_per_step = 2,target_pic_size=64):
        self.img,self.scale = self.prepare_img(img,target_pic_size)
        self.cell_size = cell_size
        self.window_size = window_size
        # 重叠率overlap = ((windw_size/cell_size) - cells_per_step)/(windw_size/cell_size)
        # cells_per_step = (1 - overlap) * windw_size / cell_size
        self.cells_per_step = cells_per_step
        self.hog_descriptor = Hog_descriptor(self.img,self.cell_size)

    def prepare_img(self,img,target_pic_size):
        img = img.astype(np.float32) / 255
        scale = img.shape[1]/target_pic_size
        img = cv2.resize(img, (np.int(img.shape[1] / scale), np.int(img.shape[0] / scale)))
        img = np.sqrt(img / np.max(img))
        img = img * 255
        return img,scale

    def split_image(self):
        # 窗口集合
        windows = []
        # 各个方向上的block数
        nxblocks = (self.img.shape[1] // self.cell_size) + 1  # -1
        nyblocks = (self.img.shape[0] // self.cell_size) + 1  # -1
        # 每个window里面几个block
        nblocks_per_window = (self.window_size // self.cell_size) - 1
        # 滑窗移动多少步，最后window到头后就不再滑动，所以少一个window的距离
        nxsteps = (nxblocks - nblocks_per_window) // self.cells_per_step
        nysteps = (nyblocks - nblocks_per_window) // self.cells_per_step
        hog = self.hog_descriptor.main()
        for xb in range(nxsteps):
            for yb in range(nysteps):
                ypos = yb * self.cells_per_step
                xpos = xb * self.cells_per_step
                # Extract HOG for this patch
                hog_features = hog[ypos:ypos + nblocks_per_window, xpos:xpos + nblocks_per_window].ravel()

                xleft = xpos * self.cell_size
                ytop = ypos * self.cell_size

                test_prediction = svc.predict(hog_features)

                if test_prediction == 1:
                    xbox_left = np.int(xleft * self.scale)
                    ytop_draw = np.int(ytop * self.scale)
                    win_draw = np.int(self.window_size * self.scale)
                    windows.append(
                        ((xbox_left, ytop_draw + 0), (xbox_left + win_draw, ytop_draw + win_draw + 0)))

        return windows