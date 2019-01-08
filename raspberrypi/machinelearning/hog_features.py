#! /usr/bin/python
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


class Hog_descriptor():
    #先算出每个像素的幅值和方向
    #然后根据cell划分算出cell内每个像素在cell中bin方向上的投影幅值
    # 把相邻4个cell合成一个block做归一化，block在x、y方向每次只移动一个cell，故block之间相互重叠
    def __init__(self, img, cell_size=16, bin_count=8,cell_perblock=2):
        self.img = img
        # 图像归一化
        # self.img = np.sqrt(img / np.max(img))
        # self.img = img * 255
        self.cell_size = cell_size
        self.bin_count = bin_count# 总共多少个bin
        self.bin_size = math.floor(360 / self.bin_count)#每个bin的角度
        self.cell_perblock = cell_perblock
        assert type(self.bin_count) == int, "bin_count should be integer,"
        assert type(self.cell_size) == int, "cell_size should be integer,"
        assert 360 % self.bin_count == 0, "bin_size should be divisible by 360"

    def global_gradient(self):
        '''
        计算每个像素的梯度和角度
        :return: 每个像素的梯度，每个像素的角度
        '''
        # dst = cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
        # 第一个参数是需要处理的图像,
        # 第二个参数是图像的深度，-1表示采用的是与原图像相同的深度。目标图像的深度必须大于等于原图像的深度；
        # dx和dy表示的是求导的阶数，0表示这个方向上没有求导，一般为0、1、2。
        # ksize是Sobel算子的大小，必须为1、3、5、7。
        # scale是缩放导数的比例常数，默认情况下没有伸缩系数；
        # delta是一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中；
        # borderType是判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。
        # Gx(x,y) = H(x+1,y)-H(x-1,y) Gy(x,y) = H(x,y+1) -H(x,y-1) 一阶导
        # angle = arctan(Gy(x,y)/Gx(x,y))，值域-180度到180度
        gradient_values_x = cv2.Sobel(self.img, cv2.CV_64F, 1, 0, ksize=5)
        gradient_values_y = cv2.Sobel(self.img, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = cv2.addWeighted(gradient_values_x, 0.5, gradient_values_y, 0.5, 0)
        gradient_angle = cv2.phase(gradient_values_x, gradient_values_y, angleInDegrees=True)
        return gradient_magnitude, gradient_angle

    def cell_gradient(self, cell_magnitude, cell_angle):
        '''
        通过像素的梯度和角度计算cell的直方图
        :param cell_magnitude: cell中每一个像素的幅值
        :param cell_angle: cell中每一个像素的角度
        :return:cell的梯度
        '''
        orientation_centers = [0] * self.bin_count
        for x in range(cell_magnitude.shape[0]):
            for y in range(cell_magnitude.shape[1]):
                # 遍历每一个胞元x,y
                gradient_strength = cell_magnitude[x][y]
                gradient_angle = cell_angle[x][y]
                min_angle, max_angle, mod = self.get_closest_bins(gradient_angle)
                # 分别投影到相邻的两个bin中
                orientation_centers[min_angle] += (gradient_strength * (1 - (mod / self.bin_size)))
                orientation_centers[max_angle] += (gradient_strength * (mod / self.bin_size))
        return orientation_centers

    def get_closest_bins(self, gradient_angle):
        '''
        计算像素在临近bin中的投影
        :param gradient_angle:
        :return:
            idx：向下取整得到的bin角度，即相邻最小的bin
            (idx + 1) % self.bin_size: 向上取整得到的bin角度，加%防止溢出，即相邻最大的bin
            mod：在当前bin中的偏移量，用于算在bin中的投影
        '''
        idx = int(gradient_angle / self.bin_size)# 第多少个bin
        mod = gradient_angle % self.bin_size
        return idx%self.bin_count, (idx + 1) % self.bin_count, mod

    def render_gradient(self, image, cell_gradient):
        '''
        归一化，画出线条查看
        :param image: 和图像同形的全零矩阵
        :param cell_gradient: 所有cell的直方图
        :return:
        '''
        cell_width = self.cell_size / 2
        max_mag = np.array(cell_gradient).max()
        for x in range(cell_gradient.shape[0]):
            for y in range(cell_gradient.shape[1]):
                cell_grad = cell_gradient[x][y]
                cell_grad /= max_mag
                angle = 0
                angle_gap = self.bin_size
                for magnitude in cell_grad:
                    angle_radian = math.radians(angle)
                    x1 = int(x * self.cell_size + magnitude * cell_width * math.cos(angle_radian))
                    y1 = int(y * self.cell_size + magnitude * cell_width * math.sin(angle_radian))
                    x2 = int(x * self.cell_size - magnitude * cell_width * math.cos(angle_radian))
                    y2 = int(y * self.cell_size - magnitude * cell_width * math.sin(angle_radian))
                    cv2.line(image, (y1, x1), (y2, x2), int(255 * math.sqrt(magnitude)))
                    angle += angle_gap
        return image

    def get_feature(self):
        height, width = self.img.shape
        #取得每个像素的梯度
        gradient_magnitude, gradient_angle = self.global_gradient()
        gradient_magnitude = abs(gradient_magnitude)
        #创建一个三维0矩阵,用来盛放每个cell
        cell_gradient_vector = np.zeros((math.floor(height / self.cell_size), math.floor(width / self.cell_size), self.bin_count))
        #遍历填充每个cell的直方图
        for x in range(cell_gradient_vector.shape[0]):
            for y in range(cell_gradient_vector.shape[1]):
                # 取出cell中每个像素的梯度和角度
                cell_magnitude = gradient_magnitude[x * self.cell_size:(x + 1) * self.cell_size,
                                 y * self.cell_size:(y + 1) * self.cell_size]
                cell_angle = gradient_angle[x * self.cell_size:(x + 1) * self.cell_size,
                             y * self.cell_size:(y + 1) * self.cell_size]
                # 计算cell的角度和梯度
                cell_gradient_vector[x][y] = self.cell_gradient(cell_magnitude, cell_angle)

        # self.hog_image = self.render_gradient(np.zeros([height, width]), cell_gradient_vector)
        hog_vector = []
        for x in range(cell_gradient_vector.shape[0] - 1):
            for y in range(cell_gradient_vector.shape[1] - 1):
                block_vector = []
                # block_vector.extend(cell_gradient_vector[x][y])
                # block_vector.extend(cell_gradient_vector[x][y + 1])
                # block_vector.extend(cell_gradient_vector[x + 1][y])
                # block_vector.extend(cell_gradient_vector[x + 1][y + 1])
                for i in range(self.cell_perblock):
                    for j in range(self.cell_perblock):
                        block_vector.extend(cell_gradient_vector[x + i][y + j])
                # 把相邻cell_perblock*cell_perblock个cell合成一个block做归一化，block在x、y方向每次只移动一个cell，故block之间相互重叠
                mag = lambda vector: math.sqrt(sum(i ** 2 for i in vector))
                magnitude = mag(block_vector)
                if magnitude != 0:
                    normalize = lambda block_vector, magnitude: [element / magnitude for element in block_vector]
                    block_vector = normalize(block_vector, magnitude)
                hog_vector.append(block_vector)
        return hog_vector

    def get_img_feature(self,target_pic_size):
        img = self.img.astype(np.float32) / 255
        # scale = img.shape[1] / target_pic_size
        img = cv2.resize(img, (np.int(target_pic_size), np.int(target_pic_size)))
        img = np.sqrt(img / np.max(img))
        self.img = img * 255
        return self.get_feature()

    def get_img(self):
        return self.img

# if __name__ == '__main__':
#     img = cv2.imread('test_images/b672637ebced7cb5ed3767e941c59c60.jpeg', cv2.IMREAD_GRAYSCALE)
#     img = np.sqrt(img / np.max(img))
#     img = img * 255
#     hog = Hog_descriptor(img, cell_size=2, bin_count=8,cell_perblock=2)
#     vector = hog.get_feature()
#     image = hog.hog_image
#     print(np.array(vector).shape)
#     plt.imshow(image, cmap=plt.cm.gray)
#     plt.show()