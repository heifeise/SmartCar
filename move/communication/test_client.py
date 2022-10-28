import client

if __name__ == '__main__':
    ip = '192.168.31.79'
    port = 6666
    clien = client.Client(ip, port)
    clien.get_connect()  # 与服务端连接
    flag = True
    while flag:
        command = input("请输入一条命令:\n")
        tag = input("请输入标识：\n")
        result = clien.send_command(tag, command)  # 发送一条命令，获取发送的结果
        print(result)
        value = eval(input("如果退出请按0,否则请按其它数字：\n"))
        if value == 0:
            flag = False
    clien.close()