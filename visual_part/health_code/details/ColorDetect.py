import cv2
import pyzbar.pyzbar as pyzbar
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def get_QR_extraction(image_input):
    """
    裁剪提取二维码，切片提取图片二维码字节对象
    """

    # 解析图片信息，decode函数提取图片中的所有二维码
    barcodes = pyzbar.decode(image_input)

    if barcodes:
        # 针对使用环境，解析识别健康码，单二维码扫描检测，取唯一的一个结果
        scan_result = barcodes[0]

        # [1] 提取当前二维码的形状
        left, top, width, height = scan_result.rect

        # （易读 + 不magic变量）
        upper_left = Point(left, top)
        lower_right = Point(left+width, top+height)

        # [2] OpenCV裁剪
        cv2.rectangle(image_input,
                      (upper_left.x, upper_left.y),
                      (lower_right.x, lower_right.y),
                      (225, 225, 225),
                      2)

        # [3] 二维码数据转换字节对象
        QR_result = image_input[
            top:top + height,
            left:left + width
        ].copy()

        # barcode_data = scann_result.data.decode("utf-8")
        # barcode_type = scann_result.type
        # # 绘出图像上条形码的数据和条形码类型
        # text = f"{barcode_data} ({barcode_type})"
        # cv2.putText(image,
        #             text,
        #             (left, top - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5,
        #             (225, 225, 225),
        #             2)
        # # 向终端打印条形码数据和条形码类型
        # print(f"[信息] 识别到 {text}")
        return QR_result
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

    return color_result


# 单模块测试
if __name__ == "__main__":
    while True:
        # 捕捉画面
        camera = cv2.VideoCapture(0)

        ret, image = camera.read()

        frame = get_QR_extraction(image)

        if frame is not None:
            cv2.imshow('video', frame)

            cv2.waitKey(6000)

            color = color_detect(frame)

            print(color)

        # 释放摄像头
        camera.release()
