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


def down_dimision(features):
    nblockx, nblocky, ncellx, ncelly, nbins = features.shape
    return features.reshape((nblockx * nblocky * ncellx * ncelly * nbins))

class HogPyramid:
    def __init__(self,img_path,initial_window_size=64,blocks_per_step = 1):
        self.img_path = img_path
        self.origin_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.initial_window_size = initial_window_size
        # 重叠率overlap = ((windw_size/cell_size) - cells_per_step)/(windw_size/cell_size)
        # cells_per_step = (1 - overlap) * windw_size / cell_size
        self.blocks_per_step = blocks_per_step
        self.svc,self.cell_size,self.cell_per_block,self.spatial_size,self.hist_bins = self.get_parameter()

    def process_image(self,img_path,scalex=1,scaley=1):
        self.hog_descriptor = Hog_descriptor(img_path, self.cell_size, self.hist_bins, self.cell_per_block)
        self.hog_descriptor.resize_pic(scale = (scalex, scaley))
        self.hog_descriptor.gamma_correct()
        self.img = self.hog_descriptor.get_img()

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
        # 各个方向上的block数
        nxblocks = (self.img.shape[1] // self.cell_size) - (self.cell_per_block - 1)  # -1
        nyblocks = (self.img.shape[0] // self.cell_size) - (self.cell_per_block - 1)  # -1
        # 每个window里面几个block
        nblocks_per_window = (window_size // self.cell_size) - (self.cell_per_block - 1)
        # 滑窗移动多少步
        nxsteps = (nxblocks//self.blocks_per_step) - (nblocks_per_window//self.blocks_per_step - 1)
        nysteps = (nyblocks // self.blocks_per_step) - (nblocks_per_window // self.blocks_per_step - 1)

        hog_features = self.hog_descriptor.get_feature()
        count = 0
        last_percentage = 0
        for xb in range(nxsteps):
            for yb in range(nysteps):
                count = count + 1
                percentage = (count / (nxsteps * nysteps))*100
                if percentage - last_percentage > 1:
                    print("completed %.2f%%"%percentage)
                    last_percentage = percentage
                ypos = yb * self.blocks_per_step * self.cell_per_block* self.cell_size
                xpos = xb * self.blocks_per_step * self.cell_per_block* self.cell_size
                features = hog_features[yb * self.blocks_per_step : yb * self.blocks_per_step + nblocks_per_window][xb * self.blocks_per_step:xb * self.blocks_per_step + nblocks_per_window]
                features_dm = down_dimision(features)
                xleft = xpos
                ytop = ypos
                try:
                    test_prediction = self.svc.predict(np.array(features_dm).reshape(1,-1))
                except ValueError:
                    test_prediction = 0

                if test_prediction == 1:
                    xbox_left = np.int(xleft)
                    ytop_draw = np.int(ytop)
                    win_draw = np.int(window_size)
                    windows.append(
                        ((xbox_left, ytop_draw + 0), (xbox_left + win_draw, ytop_draw + win_draw + 0)))

        return windows


    def search(self):
        draw_img = np.copy(self.origin_img)
        windows = []
        if self.origin_img.shape[0]>self.origin_img.shape[1]:
            level = int(math.floor(math.log((self.origin_img.shape[1]/self.initial_window_size), 2)))
        else:
            level = int(math.floor(math.log((self.origin_img.shape[0]/self.initial_window_size), 2)))

        self.img = self.origin_img
        for i in range(0,level + 1):
            image_shape_x = self.origin_img.shape[1] / (2**level)
            image_shape_y = self.origin_img.shape[0] / (2**level)
            scale_x = self.img.shape[1] / image_shape_x
            scale_y = self.img.shape[0] / image_shape_y
            self.process_image(self.img_path ,scale_x,scale_y)

            window_size = self.initial_window_size
            windows += (self.split_image(window_size))
        print(windows)
        heat_map = np.zeros(self.img.shape[:2])
        heat_map = utils.add_heat(heat_map, windows)
        heat_map_thresholded = utils.apply_threshold(heat_map, 1)
        labels = label(heat_map_thresholded)
        draw_img = utils.draw_labeled_bboxes(draw_img, labels)

        return draw_img

test_imgs=[]
out_imgs = []
img_paths = glob.glob('test_images/*.*')
plt.figure(figsize=(20,68))
for path in img_paths:
   img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
   model = HogPyramid(path)
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