from Client import Client
"""
客户端需要运行的代码
"""
"""
命令：解析
turn-left-speedleft-speedright:左转_左轮速度_右轮速度
turn-right-speedleft-speedright:右转_左轮速度_右轮速度
straight-speed:直行_速度
stop:停止
trackline:巡线模式
manual:手动控制
openDistanceMature:开启测距模块
open-image-identy:开启图像识别
"""

# list_opencv = ['open-image-identy']  # opencv相关命令
# list_action = ['turnleft', 'turnright', 'straight', 'stop', 'trackline', 'manual', 'openDistanceMature',
#                'closeDistanceMature', 'quit']  # 行动代码


if __name__ == '__main__':
    ip = '192.168.43.88'  # ### ip地址，记得改 ###
    port = [5555, 6666, 7777]
    i = 0
    clien = None
    while i != 2:
        try:
            clien = Client(ip, port[i])
            clien.get_connect()  # 与服务端连接
            break
        except ConnectionRefusedError as error:
            i += 1
    flag = True
    tag = 0
    while flag:
        try:
            command = input("请输入一条命令:\n")
            # tag = input("请输入命令标识：\n")
            tag += 1  # 自动生成命令标识
            result = clien.send_command(str(tag), command)  # 发送一条命令，获取发送的结果
            print(result)
            value = eval(input("如果退出请按0,否则请按其它数字：\n"))
            if value == 0:
                flag = False
        except ConnectionAbortedError as error:
            clien.close_connection()
            break
    clien.close_connection()
