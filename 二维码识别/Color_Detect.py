import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np


def decodeDisplay(image):  # 二维码裁剪
    barcodes = pyzbar.decode(image)  # 解析图片信息
    # print(barcodes)
    if barcodes == []:
        print("未识别到二维码")
        return None
    else:
        # print("识别到二维码")
        print(barcodes)
        for barcode in barcodes:
            # 提取二维码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
            # 提取二维码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            ROI = image[y:y + h, x:x + h].copy()
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(barcodeData, barcodeType)
            # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 225), 2)
            # 向终端打印条形码数据和条形码类型
            # print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return ROI


def color_detect(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 色彩空间的转化。转化成HSV
    height, width, _ = frame.shape
    cy, cx = height // 2, width // 2

    # 获取画面中心点像素值
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if 0 < hue_value < 11 or 156 < hue_value < 180:
        color = "RED"
    elif 11 < hue_value < 25:
        color = "ORANGE"
    elif 26 < hue_value < 34:
        color = "YELLOW"
    elif 35 < hue_value < 77:
        color = "GREEN"
    elif 78 < hue_value < 99:
        color = "Qing"
    elif 100 < hue_value < 124:
        color = "BLUE"
    elif 125 < hue_value < 155:
        color = "purple"
    # elif hue_value<170:
    #     color="PINK"
    else:
        pass
    # color="RED"
    return color


if __name__ == "__main__":
    while True:
        camera = cv2.VideoCapture(0)  # VideoCapture()中参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开
        _, image = camera.read()
        # image = cv2.imread('b.jpg')
        frame = decodeDisplay(image)

        if frame is not None:
            cv2.imshow('video', frame)
            cv2.waitKey(6000)
            color = color_detect(frame)
            print(color)
        camera.release()
        # cv2.destroyAllWindows()
