#! /usr/bin/python
# -*- coding:utf-8 -*-
from raspberrypi.machinelearning.hog_features import Hog_descriptor

def get_train_features(imgs,cell_size=8,bin_count=32,target_pic_size=64):
    features = []
    for img in imgs:
        hog_descriptor = Hog_descriptor(img,cell_size,bin_count)
        hog_feature = hog_descriptor.get_img_feature(target_pic_size)
        features.append(hog_feature)
    return features
