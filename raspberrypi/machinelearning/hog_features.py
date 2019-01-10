#! /usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np
from skimage.feature import hog


class Hog_descriptor():
    #先算出每个像素的幅值和方向
    #然后根据cell划分算出cell内每个像素在cell中bin方向上的投影幅值
    # 把相邻4个cell合成一个block做归一化，block在x、y方向每次只移动一个cell，故block之间相互重叠
    def __init__(self, img_path, cell_size=8, bin_count=11,cell_perblock=2):
        self.img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        self.cell_size = cell_size
        self.bin_count = bin_count# 总共多少个bin
        self.cell_perblock = cell_perblock
        assert type(self.bin_count) == int, "bin_count should be integer,"
        assert type(self.cell_size) == int, "cell_size should be integer,"
        assert type(self.cell_perblock) == int, "cell_perblock should be integer"

    def gamma_correct(self,gamma=0.3):
        '''
        伽马校正图片 f(I) = I^γ
        :param gamma:γ值
        :return:
        '''
        self.img = np.power(self.img / 255.0, gamma)
        self.img = self.img * 255

    def resize_pic(self,target_pic_size = None,scale = None):
        '''
        :param target_pic_size: 目标图像大小，元组，形如(x,y)
        :param scale: 缩放比例，元组，形如(x,y)
        :return:
        '''
        if target_pic_size is not None:
            self.img = cv2.resize(self.img, (np.int(target_pic_size[1]), np.int(target_pic_size[0])))
        elif scale is not None:
            self.img = cv2.resize(self.img, (np.int(self.img.shape[1]/scale[1]), np.int(self.img.shape[0]/scale[0])))

    def get_feature(self):
        features = hog(self.img, orientations=self.bin_count, pixels_per_cell=(self.cell_size, self.cell_size),
                                  cells_per_block=(self.cell_perblock, self.cell_perblock), transform_sqrt=False,
                       visualize=False, feature_vector=False)
        return features

    def get_img(self):
        return self.img

# if __name__ == '__main__':
#     import matplotlib.pyplot as plt
#     img = cv2.imread('test_images/image0000.png', cv2.IMREAD_GRAYSCALE)
#     img = np.power(img / 255.0, 0.3)
#     img = img * 255
#     from skimage.feature import hog
#     features, hog_image = hog(img, orientations=30, pixels_per_cell=(8, 8),
#                               cells_per_block=(2, 2), transform_sqrt=False,
#                               visualise=True, feature_vector=False)
#     print(features.shape)
#     plt.imshow(hog_image, cmap=plt.cm.gray)
#     plt.show()
