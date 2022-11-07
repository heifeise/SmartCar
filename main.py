import cv2
from os import system
from prompt_toolkit import prompt
from prompt_toolkit.completion.word_completer import WordCompleter
from visual_part.health_code.QR_Detectors import ColorDetector
from visual_part.mask.MaskDetect import detectFaceOpenCVDnn, if_have_mask, net


from visual_part.mask import *


def detect_color():
    while True:
        camera = cv2.VideoCapture(0)
        temp = '1'

        is_got_image, image = camera.read()

        if is_got_image:
            detector = ColorDetector(image_input=image)

            if detector.frame() is not None:
                cv2.imshow('video', image)

                cv2.waitKey(2000)

                print(detector.get_result())
                temp = input("输入任意内容以继续（q退出当前功能模块）-->>")  # 测试用

        camera.release()
        cv2.destroyAllWindows()
        if temp.lower() == 'q':
            break


def detect_mask():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    cv2.imshow('video', frame)
    cv2.waitKey(6000)
    ret, frame = detectFaceOpenCVDnn(net, frame)

    if ret == 1:
        print(if_have_mask(frame))
    else:
        print("未识别到人脸")
    
    temp = input("输入任意内容以继续（q退出当前功能模块）-->>")  # 测试用
    camera.release()
    cv2.destroyAllWindows()



def get_input_choice_index(choices: list):
    """
    对异常输入也合理处理的键盘输入选择选项
    """
    n_options = int(choices[-1])
    completion = WordCompleter(choices, ignore_case=True)
    while True:
        input_str = prompt('>>> ', completer=completion)
        if input_str.lower() in choices:
            break
        print(f"输入 {input_str} 非合理选项，请重新输入：")
    return choices.index(input_str) % n_options


def visual_part():
    while True:
        system("cls")
        print("----------------------------")
        print("-------视觉处理部分菜单-------")
        print("----------------------------")
        print("\t[1] 口罩识别")
        print("\t[2] 健康码颜色识别")
        print("\t[3] 返回")

        options = ['口罩识别', '健康码颜色识别', '返回',
                   "mask detect", "barcode color detect", "back",
                   '1', '2', '3']
        func = [detect_mask, detect_color, exit]
        option_chosen_index = get_input_choice_index(options)
        if option_chosen_index == 2:
            break
        func[option_chosen_index]()


def control_part():
    pass


def init_main_menu():
    while True:
        system("cls")
        print("----------------------------")
        print("------------菜单------------")
        print("----------------------------")
        print("----------------------------")
        print("\t[1] 视觉处理部分")
        print("\t[2] 通信与小车控制部分")
        print("\t[3] 退出程序")

        options = ['视觉处理部分', '通信与小车控制部分', '退出程序',
                   "visual part", "communication and control part", "exit",
                   '1', '2', '3']
        func = [visual_part, control_part, exit]
        option_chosen_index = get_input_choice_index(options)
        func[option_chosen_index]()


if __name__ == "__main__":
    init_main_menu()
