import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np


def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    if barcodes == []:
        print("未识别到二维码")
        return None
    else:
        print("识别到二维码")
        print(barcodes)
        for barcode in barcodes:
            # 提取二维码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
            # 提取二维码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(barcodeData, barcodeType)
            # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 225), 2)
            # 向终端打印条形码数据和条形码类型
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return image


while True:
    camera = cv2.VideoCapture(0)
    '''camera.set(3, 320)
    camera.set(4, 240)
    camera.set(5, 120)  # 设置帧率q
    # fourcc = cv2.VideoWriter_fourcc(*"MPEG")
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 40)  # 设置亮度 -64 - 64  0.0
    camera.set(cv2.CAP_PROP_CONTRAST, 50)  # 设置对比度 -64 - 64  2.0
    camera.set(cv2.CAP_PROP_EXPOSURE, 156)  # 设置曝光值 1.0 - 5000  156.0'''
    ret, image = camera.read()
    # image = cv2.imread('b.jpg')
    frame = decodeDisplay(image)
    if frame is not None:
        cv2.imshow('viedoq', frame)
        key = cv2.waitKey(6000)
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


