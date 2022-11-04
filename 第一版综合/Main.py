import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
from VisualProcess import *
if __name__ == '__main__':
    # while True:
    camera = cv2.VideoCapture(0)  # 读取相机组件
    ret, frame = camera.read()  # 从摄像头读取图像 存放在frame
    """
    cap.read()按帧读取视频，ret,frame是获cap.read()方法的两个返回值。
    其中ret是布尔值，如果读取帧是正确的则返回True，如果文件未读取到结尾，它的返回值就为False。
    frame就是每一帧的图像，是个三维矩阵。
    """
    cv2.imshow('video', frame)
    """
    cv2.imshow()函数需要两个输入，一个是图像窗口的名字即title，一个是所展示图片的像素值矩阵。
    """
    cv2.waitKey(6000)
    """
     参数是1，表示延时1ms切换到下一帧图像，参数过大如cv2.waitKey(1000)，会因为延时过久而卡顿感觉到卡顿。
     参数为0，如cv2.waitKey(0)只显示当前帧图像，相当于视频暂停。
     """

    ret, image = detectFaceOpenCVDnn(net,frame)
    """
     ret存放是否检测到人脸 如果检测到 ret==71
     frame存放经过人脸识别后 裁切出来的人脸部分图像 
    """
    if ret == 1:
        cv2.imshow('video', image)
        cv2.waitKey(6000)
        message = if_have_mask(image)
    else:
        message = "未识别到人脸"
    image = decode_display(frame)
    if image is not None:
        cv2.imshow('video', frame)
        cv2.waitKey(6000)
        color = color_detect(frame)
        # print(color)
    else:
        color = "未识别到二维码"
    print(message + "颜色" + color)
    camera.release()