from communication.Client import Client

if __name__ == '__main__':
    ip = '192.168.31.79'  # ### ip地址，记得改 ###
    port = 6666
    clien = Client(ip, port)
    clien.get_connect()  # 与服务端连接
    clien.check_connect()
    flag = True
    list_command = ['turn-left', 'turn-right', 'straight', 'trackline', 'manual', 'open-distance-manual',
                    'open-image-identy']
    while flag:
        command = input("请输入一条命令:\n")
        tag = input("请输入命令标识：\n")
        result = clien.send_command(tag, command)  # 发送一条命令，获取发送的结果
        print(result)
        value = eval(input("如果退出请按0,否则请按其它数字：\n"))
        if value == 0:
            flag = False
    clien.close()
