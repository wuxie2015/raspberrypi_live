# -*- coding: utf-8 -*-
import cv2
import time


class VideoCapture:
    def __init__(self):
        pass

    def init_camera(self):
        '''select and init camera
        0 for laptop inside camera
        1,2,3,.... for other cameras
        input: nothing
        output: videocapture object'''
        cap = cv2.VideoCapture(0)
        return cap

    def init_file(self, file_path):
        '''select the place to save your video
        input: video file path
        output: VideoWriter object'''
        try:
            out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        except AttributeError:
            out = cv2.VideoWriter(
                file_path, cv2.cv.CV_FOURCC(
                     *"XVID"), 20.0, (640, 480))
        return out

    def captuer_video(self, file_path):
        '''capture video
        input: none
        output: none'''
        self.cap = self.init_camera()
        out = self.init_file(file_path)
        # get video frame by frame
        ret, frame = self.cap.read()

        start = time.clock()
        # show your video and save
        while self.cap.isOpened():
            now = time.clock()
            if ret is True and (int(now - start) < 12):
                out.write(frame)
                # cv2.imshow("My Capture",frame)
                # # 实现按下“q”键退出程序
                # if cv2.waitKey(1)&0xFF == ord('q'):
                #     break
            else:
                break
        # release device
        # 释放摄像头资源
        self.cap.release()
        try:
            cv2.destoryAllWindows()
        except AttributeError:
            pass

    def end_rec(self):
        self.cap.release()

if __name__ == '__main__':
    vc_obj = VideoCapture()
    vc_obj.captuer_video('output.avi')
