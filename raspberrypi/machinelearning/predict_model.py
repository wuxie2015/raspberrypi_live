#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Created on Fri Oct 20 20:55:37 2017

@author: yang
"""
from raspberrypi.machinelearning.util import get_train_features
import numpy as np
import glob
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import pickle

def train():
    # 读取正负样本
    notcars = glob.glob('non-vehicles/*.png')
    cars = glob.glob('vehicles/*.png')
    # 每个cell多少像素
    pix_per_cell = 8
    # 获取汽车和非汽车的特征
    car_features = get_train_features(imgs=cars, cell_size=pix_per_cell)
    notcar_features = get_train_features(imgs=notcars, cell_size=pix_per_cell)
    # hstack沿第二轴，vstack沿第一条轴合成一个数组，如array([[ 8., 8.],[ 0., 0.]])和array([[ 1., 8.],[ 0., 4.]])
    # 通过vs是array([[ 8., 8.],[ 0., 0.],[ 1., 8.],[ 0., 4.]])，通过hstack是array([[ 8., 8., 1., 8.],[ 0., 0., 0., 4.]])
    X = np.vstack((car_features, notcar_features))
    X = X.astype(np.float64)
    # 标记数据
    y = np.hstack((np.ones(len(car_features)), np.zeros(len(notcar_features))))
    # 获取随机数种子
    rand_state = np.random.randint(0, 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=rand_state)
    #下面开始机器学习了啊，看清楚了
    svc = LinearSVC()
    svc.fit(X_train, y_train)
    # 测试集
    n_predict = 10
    print('My classfier predicts: ', svc.predict(X_test[0:n_predict]))
    print('For these', n_predict, 'labels: ', y_test[0:n_predict])
    train_dist = {}
    train_dist['clf'] = svc
    train_dist['scaler'] = None
    train_dist['orient'] = None
    train_dist['pix_per_cell'] = pix_per_cell
    train_dist['cell_per_block'] = None
    train_dist['hog_channel'] = None
    train_dist['spatial_size'] = None
    train_dist['hist_bins'] = None

    output = open('train_dist.p', 'wb')
    pickle.dump(train_dist, output)
