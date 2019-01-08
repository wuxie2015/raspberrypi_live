#! /usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import pickle
import utils
import glob
import math
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage.measurements import label
from hog_features import Hog_descriptor


# 参考https://zhuanlan.zhihu.com/p/35607432

class HogPyramid:
    def __init__(self,img,initial_window_size=64,cells_per_step = 2):
        self.img = img.astype(np.float32) / 255
        self.initial_window_size = initial_window_size
        # 重叠率overlap = ((windw_size/cell_size) - cells_per_step)/(windw_size/cell_size)
        # cells_per_step = (1 - overlap) * windw_size / cell_size
        self.cells_per_step = cells_per_step
        self.svc,self.cell_size,self.cell_per_block,self.spatial_size,self.hist_bins = self.get_parameter()

    def get_parameter(self):
        dist_pickle = pickle.load(open("train_dist.p", "rb"))
        svc = dist_pickle["clf"]
        pix_per_cell = dist_pickle["pix_per_cell"]
        cell_per_block = dist_pickle["cell_per_block"]
        spatial_size = dist_pickle["spatial_size"]
        hist_bins = dist_pickle["hist_bins"]
        return svc,pix_per_cell,cell_per_block,spatial_size,hist_bins

    def split_image(self,window_size):
        # 窗口集合
        windows = []
        # 各个方向上的cell数
        nxblocks = (self.img.shape[1] // self.cell_size) - (self.cell_per_block - 1)  # -1
        nyblocks = (self.img.shape[0] // self.cell_size) - (self.cell_per_block - 1)  # -1
        # 每个window里面几个block
        nblocks_per_window = (window_size // self.cell_size) - (self.cell_per_block - 1)
        # 滑窗移动多少步，最后window到头后就不再滑动，所以少一个window的距离
        nxsteps = (nxblocks - nblocks_per_window) // self.cells_per_step
        nysteps = (nyblocks - nblocks_per_window) // self.cells_per_step
        hog_descriptor = Hog_descriptor(self.img, self.cell_size, self.hist_bins, self.cell_per_block)
        hog_features = hog_descriptor.get_feature()
        for xb in range(nxsteps):
            for yb in range(nysteps):
                ypos = yb * self.cells_per_step * self.cell_size
                xpos = xb * self.cells_per_step * self.cell_size
                # Extract HOG for this patch
                img_splited = img[xpos :xpos+window_size, ypos:ypos + window_size]
                hog_splited = hog_features[yb * self.cells_per_step:yb * self.cells_per_step + nyblocks]
                print(np.array(hog_splited).shape)
                # hog_descriptor = Hog_descriptor(img_splited, self.cell_size, self.hist_bins, self.cell_per_block)
                # hog_features = hog_descriptor.get_img_feature(self.spatial_size)
                result = []
                for item in hog_splited:
                    result.extend(item)
                xleft = xpos
                ytop = ypos

                test_prediction = self.svc.predict(np.array(result).reshape(1,-1))

                if test_prediction == 1:
                    xbox_left = np.int(xleft)
                    ytop_draw = np.int(ytop)
                    win_draw = np.int(window_size)
                    windows.append(
                        ((xbox_left, ytop_draw + 0), (xbox_left + win_draw, ytop_draw + win_draw + 0)))

        return windows


    def search(self):
        draw_img = np.copy(self.img)

        windows = []

        # if self.img.shape[0]>self.img.shape[1]:
        #     level = int(math.floor(math.log((self.img.shape[1]/self.initial_window_size), 2)))
        # else:
        #     level = int(math.floor(math.log((self.img.shape[0]/self.initial_window_size), 2)))
        #
        # for i in range(0,level):
        #     window_size = self.initial_window_size * (2**level)
        #     if window_size == 0:
        #         window_size = self.initial_window_size
        #     windows += (self.split_image(window_size))
        window_size = self.initial_window_size
        windows += (self.split_image(window_size))
        print(windows)
        for window in windows:
            top_left = window[0]
            buttom_right = window[1]
            top_right = (buttom_right[0],top_left[1])
            buttom_left = (top_left[0],buttom_right[1])
            cv2.line(draw_img, top_left, top_right, (0, 255, 0), 5)
            cv2.line(draw_img, top_left, buttom_left, (0, 255, 0), 5)
            cv2.line(draw_img, buttom_left, buttom_right, (0, 255, 0), 5)
            cv2.line(draw_img, buttom_right, top_right, (0, 255, 0), 5)

        # heat_map = np.zeros(self.img.shape[:2])
        # heat_map = utils.add_heat(heat_map, windows)
        # heat_map_thresholded = utils.apply_threshold(heat_map, 1)
        # labels = label(heat_map_thresholded)
        # draw_img = utils.draw_labeled_bboxes(draw_img, labels)

        return draw_img

test_imgs=[]
out_imgs = []
img_paths = glob.glob('test_images/*.*')
plt.figure(figsize=(20,68))
for path in img_paths:
   img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
   model = HogPyramid(img)
   out_img = model.search()
   test_imgs.append(img)
   out_imgs.append(out_img)

plt.figure(figsize=(20,68))
for i in range(len(test_imgs)):

   # plt.subplot(2*len(test_imgs),2,2*i+1)
   # plt.imshow(test_imgs[i])
   #
   # plt.subplot(2*len(test_imgs),2,2*i+2)
   plt.imshow(out_imgs[i])
   plt.show()