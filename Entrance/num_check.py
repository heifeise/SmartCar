# 基于百度ai人流量检测
import requests
import base64
import cv2
'''
人流量统计（动态版）
'''
# 基于百度ai人流量检测
def gettoken():
    token = ""
    if token == "":
        APP_ID = '28622754'
        API_KEY = 'QATtfAeE9jZE56MsGzGlMIVl'
        SECRET_KEY = 'S47jZegomzE3GCaya5MsrLfdjc0Chmjk'

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

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
camera = cv2.VideoCapture(0)  # 读取相机组件
ret, frame = camera.read()  # 从摄像头读取图像 存放在frame
# frame = open('[本地文件]', 'rb')
img = base64.b64encode(frame)

params = {"area":"1,1,719,1,719,719,1,719","case_id":1,"case_init":"false","dynamic":"true","image":img}
access_token = gettoken()
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())