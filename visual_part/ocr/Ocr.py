# encoding:utf-8

import base64
# encoding:utf-8
import requests
import cv2


# client_id 为官网获取的AK， client_secret 为官网获取的SK
def gettoken():
    token = ""
    if token == "":
        APP_ID = '28576885'
        API_KEY = 'AN6IL1jnSVra26UeqXGYYzDe'
        SECRET_KEY = 'rXssGwS1ObhuY4qK4wpTTsdH7gBNOaTL'

        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' + \
               '&client_id=' + API_KEY + \
               '&client_secret=' + SECRET_KEY
        # print(host)
        response = requests.get(host)
        # if response:
        #     for item in response.json().items():  # 逐项遍历response.json()----字典
        #         print(item)
        token = response.json()["access_token"]
        print(">>成功获取到token")
        return token



'''
健康码识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/health_code"
camera = cv2.VideoCapture(0)  # 读取相机组件
ret, frame = camera.read()  # 从摄像头读取图像 存放在frame
# 二进制方式打开图片文件
img = base64.b64encode(frame)

params = {"image": img}
access_token = gettoken()
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())
