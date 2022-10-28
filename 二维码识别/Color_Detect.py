import cv2
import pyzbar.pyzbar as pyzbar


def decode_display(image_input):  # 二维码裁剪
    # 解析图片信息
    barcodes = pyzbar.decode(image_input)

    if barcodes:
        print(barcodes)
        for barcode in barcodes:
            # 提取二维码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image_input, (x, y), (x + w, y + h), (225, 225, 225), 2)
            # 提取二维码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            ROI = image_input[y:y + h, x:x + h].copy()
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(barcodeData, barcodeType)
            # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 225), 2)
            # 向终端打印条形码数据和条形码类型
            # print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return ROI

    return None


def color_detect(frame_input):
    hsv_frame = cv2.cvtColor(frame_input, cv2.COLOR_BGR2HSV)  # 色彩空间的转化。转化成HSV
    height, width, _ = frame_input.shape
    cy, cx = height // 2, width // 2

    # 获取画面中心点像素值
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color_result = "Undefined"
    if 0 < hue_value < 11 or 156 < hue_value < 180:
        color_result = "RED"
    elif 11 < hue_value < 25:
        color_result = "ORANGE"
    elif 26 < hue_value < 34:
        color_result = "YELLOW"
    elif 35 < hue_value < 77:
        color_result = "GREEN"
    elif 78 < hue_value < 99:
        color_result = "Qing"
    elif 100 < hue_value < 124:
        color_result = "BLUE"
    elif 125 < hue_value < 155:
        color_result = "purple"
    else:
        pass
    return color_result


if __name__ == "__main__":
    while True:
        # 捕捉画面
        camera = cv2.VideoCapture(0)
        _, image = camera.read()

        frame = decode_display(image)

        if frame is not None:
            cv2.imshow('video', frame)
            cv2.waitKey(6000)
            color = color_detect(frame)
            print(color)

        # 释放摄像头
        camera.release()
