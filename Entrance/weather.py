import requests
import ssl
from speak import espeak_chinese
ssl._create_default_https_context = ssl._create_unverified_context
def report_weather():
    myurl = "http://t.weather.sojson.com/api/weather/city/101120101" #济南市天气接口





report_weather()