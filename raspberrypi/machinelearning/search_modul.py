import aircv as ac
import cv2
import matplotlib.pyplot as plt

imsrc = ac.imread('test_images/img_0001_new.png')
imsch = ac.imread('test_images/button.png')

result = ac.find_sift(imsrc, imsch)
result_positon = result['rectangle']
src_img = cv2.imread('test_images/img_0001_new.png',cv2.COLOR_RGB2BGR)
cv2.line(src_img,result_positon[0],result_positon[1],(255,0,0),5)
cv2.line(src_img,result_positon[1],result_positon[2],(255,0,0),5)
cv2.line(src_img,result_positon[2],result_positon[3],(255,0,0),5)
cv2.line(src_img,result_positon[3],result_positon[0],(255,0,0),5)
plt.imshow(src_img)
plt.show()