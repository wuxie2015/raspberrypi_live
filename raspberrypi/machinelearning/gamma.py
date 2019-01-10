
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "zhoujuansheng"
__mtime__ = "2017/6/13"
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
# import Recognise

file_name = "test_images/image0000.png"
img = cv2.imread(file_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = np.float32(gray)
# rocg = Recognise.Recognise()
image = np.power(gray / 255.0, 1.0)
# image = rocg.gamma_rectify(gray, 0.4)
cv2.imshow("gray", gray)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
