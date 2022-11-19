import requests
import ssl
from speak import espeak_chinese
ssl._create_default_https_context = ssl._create_unverified_context
def report_weather():
    myurl = "http://t.weather.sojson.com/api/weather/city/101120101" #济南市天气接口


    response = requests.get(myurl)

    # print(response)
    json = response.json()
    # print(json)
    data = json.get("data")
    # print(data)
    temperature = data.get("wendu")
    # print(temperature)
    pm25 = data.get("pm25")
    print("temperature:{},pm25:{}".format(temperature,pm25))
    espeak_chinese("当前的温度是{}，度,当前的pm25污染指数是{}".format(temperature, pm25))


report_weather()