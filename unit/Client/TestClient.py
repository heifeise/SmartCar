"""
客户端需要运行的代码
"""
# list_opencv = ['open-image-identy']  # opencv相关命令
# list_action = ['turnleft', 'turnright', 'straight', 'stop', 'trackline', 'manual', 'openDistanceMature', 'closeDistanceMature', 'quit']  # 行动代码
from Client import Client

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
    while flag:
        try:
            command = input("请输入一条命令:\n")
            tag = input("请输入命令标识：\n")
            result = clien.send_command(tag, command)  # 发送一条命令，获取发送的结果
            print(result)
            value = eval(input("如果退出请按0,否则请按其它数字：\n"))
            if value == 0:
                flag = False
        except ConnectionAbortedError as error:
            clien._close()
            break


