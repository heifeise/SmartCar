# 基于百度ai人流量检测
import requests
import base64

'''
人流量统计（动态版）
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
frame = open('[本地文件]', 'rb')
img = base64.b64encode(frame.read())

params = {"area":"1,1,719,1,719,719,1,719","case_id":1,"case_init":"false","dynamic":"true","image":img}
access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())