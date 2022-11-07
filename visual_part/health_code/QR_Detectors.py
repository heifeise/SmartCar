import cv2
from pyzbar.pyzbar import decode
from .details import ColorDetect as detail_c_d



class ColorDetector:
    """
    健康码颜色检测接口类，不含实现细节，使用details/ColorDetect
    """

    def __init__(self, image_input) -> None:
        self.__image = image_input
        self.__QR_code_frame = self.__get_QR_extraction()
        self.__color_result = None

    def __get_QR_extraction(self):
        return detail_c_d.get_QR_extraction(self.__image)

    def __init_color_result(self):
        if self.__QR_code_frame is not None:
            self.__color_result = detail_c_d.color_detect(self.__QR_code_frame)

    def get_result(self):
        if self.__color_result is None:
            self.__init_color_result()

        return self.__color_result

    def frame(self):
        return self.__QR_code_frame


# unit-test 用
# 目前存在错误识别概率，截图利用图片正确率飙升，摄像头无论是树莓派还是电脑，均会因为反光出错    【标记】
if __name__ == "__main__":
    while True:
        camera = cv2.VideoCapture(0)

        is_got_image, image = camera.read()

        if is_got_image:
            color_detector = ColorDetector(image_input=image)
            print(color_detector.get_result())
            temp = input("输入任意内容以继续-->>")  # 测试用

        camera.release()
