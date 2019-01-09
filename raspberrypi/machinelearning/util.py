#! /usr/bin/python
# -*- coding:utf-8 -*-
from hog_features import Hog_descriptor
import cv2
import numpy as np

def get_train_features(imgs,cell_size=8,bin_count=36,target_pic_size=64,cell_perblock=2):
    features = []
    for img_item in imgs:
        result = []
        img = cv2.imread(img_item, cv2.IMREAD_GRAYSCALE)
        hog_descriptor = Hog_descriptor(img,cell_size,bin_count,cell_perblock)
        hog_feature,_ = hog_descriptor.get_img_feature(target_pic_size)
        print(np.array(hog_feature).shape)
        for item in hog_feature:
            result.extend(item)# 降维试试 todo 这里需要好好研究下
        features.append(result)
    return features
