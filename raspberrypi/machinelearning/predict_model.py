#! /usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import pickle
import glob
import math
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage.measurements import label
from hog_features import Hog_descriptor
from util import add_heat,apply_threshold,draw_labeled_bboxes
from util import get_colorful_features


# 参考https://zhuanlan.zhihu.com/p/35607432

class HogPyramid:
    def __init__(self,img_path,initial_window_size=64,cells_per_step = 1):
        self.img_path = img_path
        self.origin_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        self.colorful_img = cv2.imread(img_path)
        self.initial_window_size = initial_window_size
        # 重叠率overlap = ((windw_size/cell_size) - cells_per_step)/(windw_size/cell_size)
        # cells_per_step = (1 - overlap) * windw_size / cell_size
        self.cells_per_step = cells_per_step
        self.svc,self.cell_size,self.cell_per_block,self.spatial_size,self.hist_bins = self.get_parameter()
        self.initial_window_size = self.spatial_size

    def process_image(self,img_path,scalex=1,scaley=1):
        image = mpimg.imread(img_path)
        self.hog_descriptor_list = []
        for channel in range(image.shape[2]):
            hog_descriptor = Hog_descriptor(image[:, :, channel], self.cell_size, self.hist_bins, self.cell_per_block)
            hog_descriptor.resize_pic(scale=(scalex, scaley))
            hog_descriptor.gamma_correct()
            self.hog_descriptor_list.append(hog_descriptor.get_feature())
            self.img = hog_descriptor.get_img()


    def get_parameter(self):
        dist_pickle = pickle.load(open("train_dist.p", "rb"))
        svc = dist_pickle["clf"]
        pix_per_cell = dist_pickle["pix_per_cell"]
        cell_per_block = dist_pickle["cell_per_block"]
        spatial_size = dist_pickle["spatial_size"]
        hist_bins = dist_pickle["hist_bins"]
        return svc,pix_per_cell,cell_per_block,spatial_size,hist_bins

    def split_image(self,window_size,cur_level,total_level):
        # 窗口集合
        windows = []
        # 各个方向上的block数
        nxblocks = (self.img.shape[1] // self.cell_size) + 1  # -1
        nyblocks = (self.img.shape[0] // self.cell_size) + 1  # -1
        # 每个window里面几个block
        nblocks_per_window = (window_size // self.cell_size) - 1
        # 滑窗移动多少步
        nxsteps = (nxblocks - nblocks_per_window) // self.cells_per_step - 1
        nysteps = (nyblocks - nblocks_per_window) // self.cells_per_step - 1
        count = 0
        last_percentage = 0
        for xb in range(nxsteps):
            for yb in range(nysteps):
                features = []
                count = count + 1
                percentage = (count / (nxsteps * nysteps))*100
                if percentage - last_percentage > 1:
                    print("level %s/%s completed %.2f%%"%(cur_level,total_level,percentage))
                    last_percentage = percentage
                ypos = yb * self.cells_per_step
                xpos = xb * self.cells_per_step
                xleft = xpos * self.cell_size
                ytop = ypos * self.cell_size
                for hog in self.hog_descriptor_list:
                    features.append(hog[ypos:ypos + nblocks_per_window, xpos:xpos + nblocks_per_window])
                # features_dm = down_dimision(features)
                try:
                    test_prediction = self.svc.predict(np.array(features).ravel().reshape(1,-1))
                except ValueError as e:
                    print(xb,yb)
                    test_prediction = 0

                if test_prediction == 1:
                    xbox_left = np.int(xleft)
                    ytop_draw = np.int(ytop)
                    win_draw = np.int(window_size)
                    windows.append(
                        ((xbox_left, ytop_draw + 0), (xbox_left + win_draw, ytop_draw + win_draw + 0)))

        return windows


    def search(self):
        draw_img = np.copy(self.colorful_img)
        windows = []
        if self.origin_img.shape[0]>self.origin_img.shape[1]:
            level = int(math.floor(math.log((self.origin_img.shape[1]/self.initial_window_size), 2)))
        else:
            level = int(math.floor(math.log((self.origin_img.shape[0]/self.initial_window_size), 2)))

        self.img = self.origin_img
        # print(self.origin_img.shape)
        # for i in range(0,level + 1):
        #     scale_x = 2**i
        #     scale_y = 2**i
        #     self.process_image(self.img_path ,scale_x,scale_y)
        #     # image_shape_x = self.origin_img.shape[1] / (2 ** i)
        #     # image_shape_y = self.origin_img.shape[0] / (2 ** i)
        #     # print("image_shape_x %s,image_shape_y %s"%(image_shape_x,image_shape_y))
        #     window_size = self.initial_window_size
        #     windows += (self.split_image(window_size,i+1,level+1))
        self.process_image(self.img_path, 1.0, 1.0)
        window_size = self.initial_window_size
        windows += (self.split_image(window_size, 1, 1))
        print(windows)
        heat_map = np.zeros(self.origin_img.shape[:2])
        heat_map = add_heat(heat_map, windows)
        heat_map_thresholded = apply_threshold(heat_map, 1)
        labels = label(heat_map_thresholded)
        draw_img = draw_labeled_bboxes(draw_img, labels)

        return draw_img

    def predict_hard(self):
        features = get_colorful_features(img_path=self.img_path, cell_size=self.cell_size, bin_count=self.hist_bins,
                                         cell_perblock=self.cell_per_block)
        test_prediction = self.svc.predict(np.array(features).reshape(1, -1))
        if test_prediction == 0:
            return self.img_path


def main():
    test_imgs=[]
    out_imgs = []
    img_paths = glob.glob('test_images/*.*')

    for path in img_paths:
       img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
       model = HogPyramid(path)
       out_img = model.search()
       test_imgs.append(img)
       out_imgs.append(out_img)
       plt.figure("Image")
       plt.imshow(out_img)
       plt.show()

def predict_hard():
    img_paths = glob.glob('vehicles/*.*')
    ngtives = []
    for path in img_paths:
        model = HogPyramid(path)
        if model.predict_hard():
            ngtives.append(model.predict_hard())
    print(ngtives)


def test_parameter(windows,shape=(780,1280)):
    draw_img = np.copy(cv2.imread('test_images/test1.jpg', cv2.IMREAD_GRAYSCALE))
    heat_map = np.zeros(shape)
    heat_map = add_heat(heat_map, windows)
    heat_map_thresholded = apply_threshold(heat_map, 5000)
    right_matrix = np.ones((heat_map.shape[1],1))
    left_matrix = np.ones((1,heat_map.shape[0]))
    tmp1 = heat_map.dot(right_matrix)
    tmp2 = left_matrix.dot(tmp1)
    print(tmp2[0,0])
    labels = label(heat_map_thresholded)
    draw_img = draw_labeled_bboxes(draw_img, labels)
    plt.imshow(draw_img)
    plt.show()

if __name__ == '__main__':
    # windows = [((0, 448), (64, 512)), ((0, 456), (64, 520)), ((0, 464), (64, 528)), ((0, 472), (64, 536)), ((8, 448), (72, 512)), ((8, 456), (72, 520)), ((8, 464), (72, 528)), ((16, 448), (80, 512)), ((16, 464), (80, 528)), ((16, 656), (80, 720)), ((24, 432), (88, 496)), ((24, 448), (88, 512)), ((24, 464), (88, 528)), ((24, 656), (88, 720)), ((32, 432), (96, 496)), ((32, 448), (96, 512)), ((32, 464), (96, 528)), ((32, 656), (96, 720)), ((40, 432), (104, 496)), ((40, 440), (104, 504)), ((40, 448), (104, 512)), ((40, 464), (104, 528)), ((40, 624), (104, 688)), ((40, 640), (104, 704)), ((48, 432), (112, 496)), ((48, 440), (112, 504)), ((48, 448), (112, 512)), ((48, 464), (112, 528)), ((48, 624), (112, 688)), ((48, 640), (112, 704)), ((56, 440), (120, 504)), ((56, 448), (120, 512)), ((56, 464), (120, 528)), ((56, 624), (120, 688)), ((56, 640), (120, 704)), ((64, 440), (128, 504)), ((64, 464), (128, 528)), ((64, 624), (128, 688)), ((72, 440), (136, 504)), ((72, 464), (136, 528)), ((72, 624), (136, 688)), ((80, 440), (144, 504)), ((80, 464), (144, 528)), ((88, 464), (152, 528)), ((144, 440), (208, 504)), ((152, 424), (216, 488)), ((152, 440), (216, 504)), ((152, 456), (216, 520)), ((160, 424), (224, 488)), ((160, 440), (224, 504)), ((168, 424), (232, 488)), ((176, 424), (240, 488)), ((184, 424), (248, 488)), ((192, 424), (256, 488)), ((192, 432), (256, 496)), ((200, 424), (264, 488)), ((200, 432), (264, 496)), ((304, 248), (368, 312)), ((304, 256), (368, 320)), ((624, 392), (688, 456)), ((632, 392), (696, 456)), ((640, 392), (704, 456)), ((648, 392), (712, 456)), ((656, 392), (720, 456)), ((664,392), (728, 456)), ((712, 392), (776, 456)), ((856, 440), (920, 504)), ((856, 456), (920, 520)), ((864, 440), (928, 504)), ((872, 440), (936, 504)), ((928, 392), (992, 456)), ((928, 408), (992, 472)), ((928, 424), (992, 488)), ((928, 440), (992, 504)), ((936, 392), (1000, 456)), ((936, 400), (1000, 464)), ((936, 408), (1000, 472)), ((936, 416), (1000, 480)), ((936, 424), (1000, 488)), ((936, 440), (1000, 504)), ((944, 392), (1008, 456)), ((944, 400), (1008, 464)), ((944, 408), (1008, 472)), ((944, 416), (1008, 480)), ((944, 424), (1008, 488)), ((944, 440), (1008, 504)), ((952, 392), (1016, 456)), ((952, 400), (1016, 464)), ((952, 408), (1016, 472)), ((952, 416), (1016, 480)), ((952, 424), (1016, 488)), ((952, 440), (1016, 504)), ((960, 392), (1024, 456)), ((960, 400), (1024, 464)), ((960, 408), (1024, 472)), ((960, 416), (1024, 480)), ((960, 424), (1024, 488)), ((968, 392), (1032, 456)), ((968, 400), (1032, 464)), ((968, 408), (1032, 472)), ((968, 416), (1032, 480)), ((968, 424), (1032, 488)), ((976, 392), (1040, 456)), ((976, 400), (1040, 464)), ((976, 408), (1040, 472)), ((976, 416), (1040, 480)), ((976, 424), (1040, 488)), ((976, 432), (1040, 496)), ((976, 448), (1040, 512)), ((984, 392), (1048, 456)), ((984, 400), (1048, 464)), ((984, 408), (1048, 472)), ((984, 416), (1048, 480)), ((984, 424), (1048, 488)), ((984, 432), (1048, 496)), ((984, 448), (1048, 512)), ((992, 392), (1056, 456)), ((992, 400), (1056, 464)), ((992, 408), (1056, 472)), ((992, 416), (1056, 480)), ((992, 424), (1056, 488)), ((992, 432), (1056, 496)), ((992, 448), (1056, 512)), ((1000, 392), (1064, 456)), ((1000, 400), (1064, 464)), ((1000, 408), (1064, 472)), ((1000, 416), (1064, 480)), ((1000, 424), (1064, 488)), ((1000, 432), (1064, 496)), ((1000, 448), (1064, 512)), ((1008, 400), (1072, 464)), ((1008, 416), (1072, 480)), ((1008, 432), (1072, 496)), ((1008, 448), (1072, 512)), ((1048, 456), (1112, 520)), ((1056, 432), (1120, 496)), ((1056, 440), (1120, 504)), ((1056, 448), (1120, 512)), ((1056, 456), (1120, 520)), ((1056, 472), (1120, 536)), ((1064, 424), (1128, 488)), ((1064, 432), (1128, 496)), ((1064, 440), (1128, 504)), ((1064, 448), (1128, 512)), ((1064, 456), (1128, 520)), ((1064, 464), (1128, 528)), ((1064, 472), (1128, 536)), ((1072, 424), (1136, 488)), ((1072, 432),(1136, 496)), ((1072, 440), (1136, 504)), ((1072, 448), (1136, 512)), ((1072, 456), (1136, 520)), ((1072, 472), (1136, 536)), ((1080, 432), (1144, 496)), ((1128, 456), (1192, 520)), ((1128, 464), (1192, 528)), ((1128, 472), (1192, 536)), ((1128, 488), (1192, 552)), ((1136, 408), (1200, 472)), ((1136, 448), (1200, 512)), ((1136, 456), (1200, 520)), ((1136, 464), (1200, 528)), ((1136, 472), (1200, 536)), ((1136, 480), (1200, 544)), ((1136, 488), (1200, 552)), ((1144, 408), (1208, 472)), ((1144, 424), (1208, 488)), ((1144, 448), (1208, 512)), ((1144, 456), (1208, 520)), ((1144, 472), (1208, 536)), ((1144, 488), (1208, 552)), ((1152, 408), (1216, 472)), ((1152, 424), (1216, 488)), ((1152, 448), (1216, 512)), ((1152, 456), (1216, 520)), ((1160, 408), (1224, 472)), ((1160, 424), (1224, 488)), ((1160, 456), (1224, 520)), ((1168, 408), (1232, 472)), ((1168, 424), (1232, 488)), ((1168, 456), (1232, 520)), ((1176, 408), (1240, 472)), ((1176, 424), (1240, 488)), ((1176, 440), (1240, 504)), ((1176, 456), (1240, 520)), ((1184, 408), (1248, 472)), ((1184, 424), (1248, 488)), ((1184, 432), (1248, 496)), ((1184, 440), (1248, 504)), ((1184, 456), (1248, 520)), ((1192, 408), (1256, 472)), ((1192, 424), (1256, 488)), ((1192, 432), (1256, 496)), ((1192, 440), (1256, 504)), ((1192, 456), (1256, 520)), ((1200, 424), (1264, 488)), ((1200, 432), (1264, 496)), ((1200, 440), (1264, 504)), ((1200, 456), (1264, 520)), ((1208, 424), (1272, 488)), ((416, 208), (480, 272)), ((464, 176), (528, 240)), ((464, 184), (528, 248)), ((464, 192), (528, 256)), ((464, 208), (528, 272)), ((472, 176), (536, 240)), ((472, 184), (536, 248)), ((472, 192), (536, 256)), ((472, 208), (536, 272)), ((480, 192), (544, 256)), ((552, 200), (616, 264)), ((560, 192), (624, 256)), ((560, 200), (624, 264)), ((560, 208), (624, 272)), ((568, 192), (632, 256)),((568, 200), (632, 264)), ((568, 208), (632, 272)), ((568, 224), (632, 288)), ((576, 200), (640, 264))]
    # test_parameter(windows)
    main()
    # predict_hard()
