#! /usr/bin/python
# -*- coding:utf-8 -*-
from hog_features import Hog_descriptor
import cv2
import numpy as np

def get_train_features(imgs,cell_size=8,bin_count=36,target_pic_size=(64,64),cell_perblock=2):
    features = []
    for img_item in imgs:
        hog_descriptor = Hog_descriptor(img_item,cell_size,bin_count,cell_perblock)
        hog_descriptor.resize_pic(target_pic_size)
        hog_descriptor.gamma_correct()
        hog_feature = hog_descriptor.get_feature()
        features.append(hog_feature)
    return np.array(features)
