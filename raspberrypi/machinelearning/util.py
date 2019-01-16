#! /usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import matplotlib.image as mpimg
from hog_features import Hog_descriptor

def get_train_features(imgs,cell_size=8,bin_count=36,target_pic_size=(64,64),cell_perblock=2):
    features = []
    for img_item in imgs:
        features.append(get_colorful_features(img_item,cell_size,bin_count,target_pic_size,cell_perblock))
    return features

def get_colorful_features(img_path,cell_size=8,bin_count=36,target_pic_size=(64,64),cell_perblock=2):
    hog_features = []
    image = mpimg.imread(img_path)
    for channel in range(image.shape[2]):
        hog_descriptor = Hog_descriptor(image[:,:,channel], cell_size, bin_count, cell_perblock)
        hog_descriptor.resize_pic(target_pic_size)
        hog_descriptor.gamma_correct()
        hog_features.append(hog_descriptor.get_feature())
    hog_features = np.ravel(hog_features)
    return hog_features

def add_heat(heatmap, bbox_list):
    # Iterate through list of bboxes
    for box in bbox_list:
        # Add += 1 for all pixels inside each bbox
        # Assuming each "box" takes the form ((x1, y1), (x2, y2))
        heatmap[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1

    # Return updated heatmap
    return heatmap

def apply_threshold(heatmap, threshold):
    # Zero out pixels below the threshold
    heatmap[heatmap <= threshold] = 0
    # Return thresholded map
    return heatmap

def draw_labeled_bboxes(img, labels):
    # Iterate through all detected cars
    for car_number in range(1, labels[1]+1):
        # Find pixels with each car_number label value
        nonzero = (labels[0] == car_number).nonzero()
        # Identify x and y values of those pixels
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Define a bounding box based on min/max x and y
        bbox = ((np.min(nonzerox), np.min(nonzeroy)), (np.max(nonzerox), np.max(nonzeroy)))
        # Draw the box on the image
        cv2.rectangle(img, bbox[0], bbox[1], (0,0,255), 6)
    # Return the image
    return img